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

import os
import logging
import copy
import warnings
from pathlib import Path
from typing import List, Optional, Tuple, Union

import torch
import torch.nn.functional as F
from tqdm import tqdm
from transformers import AutoTokenizer, BatchEncoding, T5Tokenizer


logger = logging.getLogger(__name__)

TokenSequence = Union[List[int], torch.LongTensor, torch.Tensor, BatchEncoding]


def generate_batches(batch, batch_size):
    start = 0
    while start < len(batch):
        end = start + batch_size
        yield batch[start:end]
        start = end


class TRTLLM:
    def __init__(
        self,
        tokenizer: str,
        engine_dir: str,
        **kwargs,
    ):
        super().__init__()

        import tensorrt_llm
        from tensorrt_llm.runtime import ModelRunner

        assert isinstance(tokenizer, str)
        assert isinstance(engine_dir, str)

        self.tokenizer = self.get_tokenizer(tokenizer)
        self.runtime_rank = tensorrt_llm.mpi_rank()
        runner_kwargs = dict(engine_dir=engine_dir, rank=self.runtime_rank, **kwargs)
        self.runner = ModelRunner.from_dir(**runner_kwargs)

        logger.info("Loaded TRT-LLM engine")

    @staticmethod
    def get_tokenizer(tokenizer: str):
        try:
            tokenizer = AutoTokenizer.from_pretrained(tokenizer, trust_remote_code=True)
        except Exception:
            logger.warn('Loading in AutoTokenizer mode failed. Trying to load as a SentencePiece tokenizer')
            try:
                tokenizer = T5Tokenizer(tokenizer)
            except Exception:
                raise Exception('Corrupted SentencePiece tokenizer file or tokenizer type unsupported')
        logger.info("Loaded tokenizer")
        if tokenizer.pad_token_id is None:
            tokenizer.pad_token_id = tokenizer.eos_token_id
        return tokenizer

    @property
    def eot_token_id(self):
        try:
            return self.tokenizer.eos_id
        except AttributeError:
            return None

    @property
    def max_gen_toks(self):
        return self._max_gen_toks

    @property
    def max_length(self):
        raise NotImplementedError("TODO: add 'max_length' argument to TRTLLM model")

    @property
    def batch_size(self):
        return self._batch_size

    def tok_encode(self, string: str):
        return self.tokenizer.encode(string, add_special_tokens=False)

    def tok_encode_batch(self, strings: List[str]) -> TokenSequence:
        return [
            torch.IntTensor(self.tok_encode(s)) for s in strings
        ]

    def tok_decode(self, tokens):
        return self.tokenizer.batch_decode(tokens, skip_special_tokens=True)

    def _generate(self, input_tokens, max_tokens: int, until: List[str], **generation_kwargs: dict) -> dict:
        with torch.no_grad():
            outputs = self.runner.generate(
                input_tokens,
                max_new_tokens=max_tokens,
                end_id=self.tokenizer.eos_token_id,
                pad_id=self.tokenizer.pad_token_id,
                stop_words_list=until,
                return_dict=True,
                **generation_kwargs,
            )
        torch.cuda.synchronize()
        return outputs

    def _encode_pair(self, context, continuation):
        n_spaces = len(context) - len(context.rstrip())
        if n_spaces > 0:
            continuation = context[-n_spaces:] + continuation
            context = context[:-n_spaces]
        whole_enc = self.tok_encode(context + continuation)
        context_enc = self.tok_encode(context)
        context_enc_len = len(context_enc)
        continuation_enc = whole_enc[context_enc_len:]
        return context_enc, continuation_enc

    def generate(
        self,
        input_text: str,
        max_length: int,  # prompt + generation
        temperature: float,
        top_k: int,
        top_p: float,
        num_sequences: int = 1,
        batch_size: int = 1,
        **kwargs,
        ):
        assert num_sequences > 0

        tokens = self.tok_encode(input_text)
        if len(tokens) >= max_length:
            warnings.warn("The number of tokens >= `max_length`. Returning inputs without completions.")
            return [input_text] * num_sequences


        tokens_to_generate = max_length - len(tokens)
        input_texts = [input_text] * num_sequences
        batches = list(generate_batches(input_texts, batch_size))

        results = []

        for batch in tqdm(
            batches,
            desc="TRTLLM.generate",
        ):
            context = [
                torch.tensor(self.tok_encode(text), dtype=torch.int32) for text in batch
            ]
            stop_words_list = None

            outputs = self._generate(
                context,
                tokens_to_generate,
                stop_words_list,
                temperature=temperature,
                top_p=top_p,
                top_k=top_k,
            )  # (batch_size, num_beams = 1)
            token_ids = outputs['output_ids']
            # shape: (batch, beams, tokens)
            assert token_ids.shape[1] == 1, token_ids.shape
            responses = self.tok_decode(outputs['output_ids'][:, 0])
            results.extend(responses)

        return results
