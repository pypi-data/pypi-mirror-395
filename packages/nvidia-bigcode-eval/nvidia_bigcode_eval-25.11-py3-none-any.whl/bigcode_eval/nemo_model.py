# SPDX-FileCopyrightText: Copyright (c) 2025 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import warnings

import numpy as np
import torch

import importlib
import pathlib
from tqdm import tqdm
from typing import List, Optional

import filelock


class TokenizerWrapper:
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer
    
    @property
    def eos_token(self) -> str:
        return "<|endoftext|>"

    def __call__(self, texts, *args, **kwargs):
        tokens = np.asarray([np.asarray(self.text_to_ids(text)) for text in texts])
        return TokenizerOutput(tokens)

    def __getattr__(self, name):
        return getattr(self.tokenizer, name)


class TokenizerOutput:
    def __init__(self, tokenized_batch_ids):
        self.input_ids = tokenized_batch_ids
        self.attention_mask = np.asarray([
            np.asarray([True] * len(tokenized_batch_ids[i]))
            for i in range(len(tokenized_batch_ids))
        ])


def _patch_pretrained_cfg(pretrained_cfg, trainer, tensor_model_parallel_size, pipeline_model_parallel_size):
    import omegaconf

    omegaconf.OmegaConf.set_struct(pretrained_cfg, True)
    with omegaconf.open_dict(pretrained_cfg):
        attributes_to_update = {
            "sequence_parallel": False,
            "activations_checkpoint_granularity": None,
            "activations_checkpoint_method": None,
            "precision": trainer.precision,
            "global_batch_size": None,
            "tensor_model_parallel_size": tensor_model_parallel_size,
            "pipeline_model_parallel_size": pipeline_model_parallel_size,
        }
        for name, value in attributes_to_update.items():
            if hasattr(pretrained_cfg, name):
                pretrained_cfg[name] = value
    return pretrained_cfg


def _get_target_from_class(target_class) -> str:
    return f"{target_class.__module__}.{target_class.__name__}"


def load_model(model_path: str, trainer, tensor_model_parallel_size, pipeline_model_parallel_size) -> torch.nn.Module:
    from nemo.collections.nlp.models.language_modeling.megatron_gpt_model import MegatronGPTModel
    from nemo.collections.nlp.parts.nlp_overrides import NLPSaveRestoreConnector

    model_path = pathlib.Path(model_path)

    save_restore_connector = NLPSaveRestoreConnector()
    if model_path.is_dir():
        save_restore_connector.model_extracted_dir = model_path.as_posix()
    pretrained_cfg = save_restore_connector.restore_from(
        None, model_path.as_posix(), return_config=True, trainer=trainer
    )
    if not hasattr(pretrained_cfg, "target"):
        pretrained_cfg["target"] = _get_target_from_class(MegatronGPTModel)

    pretrained_cfg = _patch_pretrained_cfg(
        pretrained_cfg, trainer,
        tensor_model_parallel_size=tensor_model_parallel_size,
        pipeline_model_parallel_size=pipeline_model_parallel_size,
    )
    model_to_load_path = model_path
    override_config = pretrained_cfg

    module_name, class_name = override_config.target.rsplit(".", 1)
    model_class = getattr(importlib.import_module(module_name), class_name)

    # monkeypatch _build_tokenizer method to be process-safe
    tokenizer_lock = filelock.FileLock(f"/tmp/{model_path.name}.tokenizer.lock")

    def _synced_build_tokenizer(self):
        with tokenizer_lock:
            self._original_build_tokenizer()

    model_class._original_build_tokenizer = model_class._build_tokenizer
    model_class._build_tokenizer = _synced_build_tokenizer

    model = model_class.restore_from(
        restore_path=model_to_load_path.as_posix(),
        trainer=trainer,
        override_config_path=override_config,
        save_restore_connector=save_restore_connector,
        map_location=f'cuda:{trainer.local_rank}',
    )

    model.freeze()
    model.training = False
    try:
        # Have to turn off activations_checkpoint_method for inference
        model.model.language_model.encoder.activations_checkpoint_method = None
    except AttributeError:
        pass
    return model


def setup_distributed_environment(trainer):
    from nemo.utils.app_state import AppState
    def dummy():
        return

    if trainer.strategy.launcher is not None:
        trainer.strategy.launcher.launch(dummy, trainer=trainer)
    trainer.strategy.setup_environment()

    app_state = AppState()

    return app_state


def generate_batches(batch, batch_size):
    start = 0
    while start < len(batch):
        end = start + batch_size
        yield batch[start:end]
        start = end


class NeMoGPT3LM:

    def __init__(
            self,
            path,
            tensor_model_parallel_size=torch.cuda.device_count(),
            pipeline_model_parallel_size=1,
            precision="bf16",
            add_bos_token: bool = False,
            **kwargs
        ):
        super().__init__()

        from pytorch_lightning.trainer.trainer import Trainer
        from nemo.collections.nlp.parts.nlp_overrides import NLPDDPStrategy

        trainer = Trainer(
            strategy=NLPDDPStrategy(),
            devices=tensor_model_parallel_size,
            accelerator="gpu",
            num_nodes=pipeline_model_parallel_size,
            precision=precision,
            logger=False,
            enable_checkpointing=False,
            use_distributed_sampler=False,
        )

        self.model = load_model(
            path, trainer,
            tensor_model_parallel_size=tensor_model_parallel_size,
            pipeline_model_parallel_size=pipeline_model_parallel_size,
        ).cuda()
        self.tokenizer = TokenizerWrapper(self.model.tokenizer)
        self.app_state = setup_distributed_environment(trainer)
        self.add_bos_token = add_bos_token

    def tok_encode(self, string: str):
        return self.tokenizer.text_to_ids(string)

    def tok_decode(self, tokens):
        return self.tokenizer.ids_to_text(tokens)
    
    def generate(
            self,
            input_text: str,
            do_sample: bool,
            max_length: int,  # prompt + generation
            temperature: float,
            top_k: int,
            top_p: float,
            num_sequences: int = 1,
            batch_size: int = 1,
            end_strings: Optional[List[str]] = None,
            max_new_tokens: Optional[int] = None,
        ):
        from nemo.collections.nlp.modules.common.text_generation_utils import generate

        assert num_sequences > 0

        tokens = self.tok_encode(input_text)
        if len(tokens) >= max_length:
            warnings.warn("The number of tokens >= `max_length`. Returning inputs without completions.")
            return [input_text] * num_sequences

        if max_new_tokens is None:
            max_new_tokens = max_length - len(tokens)

        input_texts = [input_text] * num_sequences

        if max_new_tokens == 0:
            warnings.warn("tokens_to_generate = 0: returning the inputs")
            return input_texts

        greedy = not do_sample

        end_strings = (end_strings or []) + [self.tokenizer.eos_token]
        batches = list(generate_batches(input_texts, batch_size))
        
        outputs = []
        for batch in tqdm(batches, desc="NeMoGPT3LM.generate"):
            outputs.extend(
                generate(
                    self.model,
                    inputs=batch,
                    tokens_to_generate=max_new_tokens,
                    end_strings=end_strings,
                    greedy=greedy,
                    temperature=temperature,
                    add_BOS=self.add_bos_token,
                    top_k=top_k,
                    top_p=top_p,
                )["sentences"]
            )
        return outputs
