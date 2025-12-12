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
import argparse
import json
from pathlib import Path

from bigcode_eval.utils import make_instruction_prompt, batched_iterable
from bigcode_eval.server.nim import NIMCompletion, NIMChat
from bigcode_eval.server.nvcf import NVCFCompletion, NVCFChat
from bigcode_eval import tasks
from tqdm import tqdm
import logging

from bigcode_eval.parsing_utils import str2bool, str2json

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_type", choices=["nim-base", "nim-chat", "nvcf-base", "nvcf-chat"], required=True)
    parser.add_argument("--url", type=str, default=None)
    parser.add_argument("--model_kwargs", type=str2json, default=None, 
                        help="""Passed as a JSON string representing the model kwargs that will
                          be used in model intitialisation""")
    parser.add_argument("--gen_kwargs", type=str2json, default=None, 
                        help="""Passed as a JSON string representing the extra generation
                          kwargs that will be used in requests.""")
    parser.add_argument("--max_length", type=int, default=4096, 
                        help="""Corresponds to the  max length of the input prompt + generated tokens. 
                        If the input prompt is larger than max_length - max_new_tokens the prompt will be 
                        truncated. Will be ignored for tasks constructed as list of messages e.g. bfcl.""")
    parser.add_argument("--until", type=str, default=None)
    parser.add_argument("--do_sample", type=str2bool, default=True, choices=[False, True])
    parser.add_argument("--n_samples", type=int, default=1)
    parser.add_argument("--temperature", type=float, default=1.0)
    parser.add_argument("--top_p", type=float, default=1.0)
    parser.add_argument("--task", required=True)
    parser.add_argument("--task_kwargs", type=str2json, default=None, 
                        help="""Passed as a JSON string representing the task kwargs that will
                          be used in task intitialisation""")
    parser.add_argument("--max_new_tokens", type=int, help="The maximum number of tokens that can be generated in the chat completion.", default=512)
    parser.add_argument("--out_dir", required=True)
    parser.add_argument("--limit_start", type=int, default=0)
    parser.add_argument("--limit", type=int)
    parser.add_argument("--debug", action="store_true", help="set logging level to debug, useful for tracking sent requests")
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
        "--save_every_k_tasks",
        type=int,
        default=1,
        help="Saving after every k tasks",
    )
    parser.add_argument(
        "--async_limit",
        type=int,
        default=20,
        help="Asynchronous requests limit, if n_samples = 1 it will be used as batch size",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    out_dir = Path(args.out_dir)

    logging.basicConfig(level=logging.INFO if not args.debug else logging.DEBUG)
    if not args.generation_only and not args.allow_code_execution:
        raise ValueError("To evaluate the generation, you must pass --allow_code_execution")

    if args.model_type in ["base", "chat"] and not args.url:
        raise ValueError("You need to provide URL for NIM model class")

    local_rank = int(os.environ.get("LOCAL_RANK", 0))

    task = tasks.get_task(args.task, args)
    dataset = task.get_dataset()

    if args.limit_start is not None and args.limit is not None:
        dataset = [
            dataset[i]
            for i in range(args.limit_start, min(args.limit_start + args.limit, len(dataset)))
        ]
    docs = [doc for doc in dataset]

    model_cls = {
        "nim-base": NIMCompletion,
        "nim-chat": NIMChat,
        "nvcf-base": NVCFCompletion,
        "nvcf-chat": NVCFChat,
    }[args.model_type]
    generations = []

    if (out_dir / "predictions.json").exists():
        # suspend-resume
        with open(out_dir / "predictions.json") as fp:
            generations = json.load(fp)
        start_idx = len(generations)
        docs_to_process = docs[start_idx:]
        
    else:
        docs_to_process = docs
        start_idx = (args.limit_start or 0)
    model = model_cls(
        url=args.url,
        max_length=args.max_length,
        temperature=args.temperature,
        top_p=args.top_p,
        async_limit=args.async_limit,
        **args.model_kwargs,
    )
    batch_size = 1 if args.n_samples > 1 else args.async_limit
    for i, batch_docs in tqdm(enumerate(batched_iterable(docs_to_process, batch_size)), total=(len(docs_to_process) + batch_size - 1) // batch_size):
        # Create a list of prompts for the batch
        prompts = []
        for doc in batch_docs:
            prompt = task.get_prompt(doc)
            
            if isinstance(prompt, dict):
                prompt_keys = set(prompt.keys())
                
                if prompt_keys == {"instruction", "context"}:
                    prompt = make_instruction_prompt(**prompt, instruction_tokens=("", "", ""))
                else:
                    raise ValueError(f"Tasks with keys {prompt_keys} are not supported.")
            
            # Append the processed prompt to the prompts list
            prompts.append(prompt)
        if args.n_samples > 1:
            prompts = prompts * args.n_samples
        
        # Generate responses for the entire batch of prompts
        gens = model.generate(
            input_texts=prompts,  # Now prompts is a list of inputs
            do_sample=args.do_sample,
            num_sequences=args.n_samples,
            max_gen_tokens=args.max_new_tokens,
            until=args.until.split(",") if args.until else [],
            gen_kwargs=args.gen_kwargs
        )
        if args.n_samples > 1:
            gens = [
                task.postprocess_generation(g, start_idx + i)
                for g in gens
            ]
            generations.append(gens)
        else:
            gens = [
                task.postprocess_generation(g, start_idx + i * batch_size + j)
                for j, g in enumerate(gens)
            ]
            generations.extend([[g] for g in gens])

        if args.save_every_k_tasks > 0 and (i + 1) % args.save_every_k_tasks == 0 and local_rank == 0:
            with open(out_dir / "predictions.json", "w") as fp:
                json.dump(generations, fp)

    if local_rank == 0:
        out_dir.mkdir(exist_ok=True)

        with open(out_dir / "predictions.json", "w") as fp:
            json.dump(generations, fp)

        task = tasks.get_task(args.task, args)
        dataset = task.get_dataset()

        if not args.generation_only:
            os.environ["HF_ALLOW_CODE_EVAL"] = "1"
            references = [task.get_reference(doc) for doc in docs]
            metrics = task.process_results(generations, references)
            results = {
                args.task: metrics,
                "config": vars(args),
            }
            with open(out_dir / "metrics.json", "w") as fp:
                json.dump(results, fp, indent=4, sort_keys=False)
            print(json.dumps(results, indent=4))


if __name__ == "__main__":
    main()
