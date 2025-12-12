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

# NOTE(dfridman): entrypoint for NeMo and TRT-LLM models

import os
import argparse
import json
import logging
from pathlib import Path
from typing import Dict, List

import torch
from tqdm import tqdm

from bigcode_eval.nemo_model import NeMoGPT3LM
from bigcode_eval.trtllm_model import TRTLLM
from bigcode_eval.utils import make_instruction_prompt
from bigcode_eval import tasks
from bigcode_eval import logger


def get_model_cls(model_cls_name):
    name_to_model_cls = {
        "nemo": NeMoGPT3LM,
        "trt-llm": TRTLLM,
    }
    return name_to_model_cls[model_cls_name]


def parse_model_arg_string(args_string):
    """
    Parses something like
        args1=val1,arg2=val2
    Into a dictionary
    """
    # https://gitlab-master.nvidia.com/dfridman/lm-evaluation-harness/-/blob/llm-bench/lm_eval/utils.py?ref_type=heads#L64
    args_string = args_string.strip()
    if not args_string:
        return {}
    arg_list = [arg for arg in args_string.split(",") if arg]
    args_dict = {
        k: handle_arg_string(v) for k, v in [arg.split("=") for arg in arg_list]
    }
    return args_dict


def handle_arg_string(arg):
    # https://gitlab-master.nvidia.com/dfridman/lm-evaluation-harness/-/blob/llm-bench/lm_eval/utils.py?ref_type=heads#L51
    if arg.lower() == "true":
        return True
    elif arg.lower() == "false":
        return False
    elif arg.isnumeric():
        return int(arg)
    try:
        return float(arg)
    except ValueError:
        return arg


def str2bool(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def get_rank():
    if torch.distributed.is_available() and torch.distributed.is_initialized():
        rank = torch.distributed.get_rank()
    else:
        rank = os.getenv("LOCAL_RANK", 0)
    return int(rank)


def cache_generations(generations, out_path: Path):
    out_path.parent.mkdir(exist_ok=True, parents=True)
    with open(out_path, "w") as fp:
        json.dump(generations, fp)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_type", choices=["nemo", "trt-llm"], required=True)
    parser.add_argument(
        "--model_args",
        default="",
        help="Comma separated string arguments for model, e.g. `pretrained=EleutherAI/pythia-160m,dtype=float32`",
    )
    parser.add_argument("--batch_size", type=int, required=True)
    parser.add_argument("--n_samples", type=int, default=1)
    parser.add_argument("--do_sample", type=str2bool, default=True, choices=[False, True])
    parser.add_argument("--top_p", type=float, default=0)
    parser.add_argument("--top_k", type=int, default=0)
    parser.add_argument("--temperature", type=float, default=1.0)
    parser.add_argument("--task", required=True)
    parser.add_argument("--max_length_generation", type=int, default=512)
    parser.add_argument("--max_new_tokens", type=int, help="The maximum number of tokens that can be generated in the completion.", default=None)
    parser.add_argument("--out_dir", required=True)
    parser.add_argument("--limit_start", type=int)
    parser.add_argument("--limit", type=int)
    parser.add_argument(
        "--generation_only",
        action="store_true",
        help="Do code generation but no evaluation",
    )
    parser.add_argument(
        "--allow_code_execution",
        action="store_true",
        help="Allow code evaluation to execute external/untrusted Python code on your machine",
    )
    parser.add_argument(
        "--chat_template",
        default=None,
        help="path to a file or a jinja string defining chat template",
    )
    return parser.parse_args()


class ChatTemplate:
    def __init__(self, chat_template: str) -> None:
        from jinja2.exceptions import TemplateError
        from jinja2.sandbox import ImmutableSandboxedEnvironment

        self.template_str = chat_template

        def raise_exception(message):
            raise TemplateError(message)

        jinja_env = ImmutableSandboxedEnvironment(trim_blocks=True, lstrip_blocks=True)
        jinja_env.policies["json.dumps_kwargs"]["ensure_ascii"] = False
        jinja_env.globals["raise_exception"] = raise_exception
        self.compiled_template = jinja_env.from_string(chat_template)

    def __call__(self, messages: List[Dict[str, str]], add_generation_prompt: bool = False):
        return self.compiled_template.render(
            messages=messages,
            add_generation_prompt=add_generation_prompt,
        )


def main():
    args = parse_args()

    if not args.generation_only and not args.allow_code_execution:
        raise ValueError("To evaluate the generation, you must pass --allow_code_execution")

    rank = get_rank()

    task = tasks.get_task(args.task)
    dataset = task.get_dataset()

    if args.limit_start is not None and args.limit is not None:
        dataset = [
            dataset[i]
            for i in range(args.limit_start, min(args.limit_start + args.limit, len(dataset)))
        ]
    docs = [doc for doc in dataset]

    model_cls = get_model_cls(args.model_type)
    model_args = parse_model_arg_string(args.model_args)
    model = model_cls(**model_args)

    # NOTE(dfridman): suspend-resume logic
    predictions_filepath = Path(args.out_dir) / "predictions.json"
    if predictions_filepath.exists():
        with open(predictions_filepath) as fp:
            generations = json.load(fp)
        assert len(generations) <= len(docs)
        offset = len(generations)

    else:
        generations = []
        offset = 0

    if args.chat_template is not None:
        if os.path.exists(args.chat_template):
            with open(args.chat_template) as f:
                template_str = f.read()
            logging.info(f"Loaded chat template from {args.chat_template} file")
        else:
            template_str = args.chat_template
            logging.info(f"Using {args.chat_template} as chat template")
        chat_template = ChatTemplate(template_str)
    else:
        chat_template = None

    for i, doc in tqdm(enumerate(docs[offset:], start=offset), total=len(docs) - offset):
        prompt = task.get_prompt(doc)
        if isinstance(prompt, dict):
            assert set(prompt.keys()) == {"instruction", "context"}, f"Expected 'instruction' and 'context' keys, got {set(prompt.keys())} instead"
            if chat_template is not None:
                chat = [{"role": "user", "content": prompt["instruction"]}]
                formatted_prompt = chat_template(chat, add_generation_prompt=True) + prompt["context"]
            else:
                formatted_prompt = make_instruction_prompt(**prompt, instruction_tokens=("", "", "\n"))
            start_idx = len(formatted_prompt) - len(prompt["context"])
            prompt = formatted_prompt
        else:
            start_idx = 0

        gens = model.generate(
            input_text=prompt,
            do_sample=args.do_sample,
            temperature=args.temperature,
            top_k=args.top_k,
            top_p=args.top_p,
            max_length=args.max_length_generation,
            max_new_tokens=args.max_new_tokens,
            num_sequences=args.n_samples,
            batch_size=args.batch_size,
        )
        gens = [
            task.postprocess_generation(g[start_idx:], (args.limit_start or 0) + i)
            for g in gens
        ]
        generations.append(gens)
        if rank == 0:
            cache_generations(generations, predictions_filepath)

    if rank == 0:
        if len(args.out_dir) > 0:
            os.makedirs(args.out_dir, exist_ok=True)

        with open(os.path.join(args.out_dir, "predictions.json"), "w") as fp:
            json.dump(generations, fp)

        if not args.generation_only:
            os.environ["HF_ALLOW_CODE_EVAL"] = "1"
            references = [task.get_reference(doc) for doc in docs]
            metrics = task.process_results(generations, references)
            results = {
                args.task: metrics,
                "config": vars(args),
            }
            with open(os.path.join(args.out_dir, "metrics.json"), "w") as fp:
                json.dump(results, fp, indent=4, sort_keys=False)
            print(json.dumps(results, indent=4))



if __name__ == "__main__":
    main()
