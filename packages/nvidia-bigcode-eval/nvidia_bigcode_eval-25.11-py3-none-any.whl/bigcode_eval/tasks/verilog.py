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

"""
VerilogEval: Evaluating Large Language Models for Verilog Code Generation
Paper: https://arxiv.org/abs/2309.07544
GitHub: https://github.com/NVlabs/verilog-eval

VerilogEval consists of two datasets:
1) VerilogEval-human - 156 problems
2) VerilogEval-machine - 143 problems
All problems involve generating self-contained Verilog modules.
The machine dataset is more verbose and may contain ambiguity and errors but it's useful for
"assessing LLM's competence in comprehending low-level instructions and generating syntactically and
functionally accurate Verilog code".

To verify correctness of generated solution, we create Verilog program with provided code for testing
and Verilog module completed by LLM, and execute it using the ICARUS Verilog simulator.
"""

from bigcode_eval.base import Task
from bigcode_eval.tasks.custom_metrics.code_eval import compute_code_eval
from bigcode_eval.tasks.custom_metrics.verilog_execute import check_correctness as verilog_correctness

import json, warnings

_CITATION = """
@inproceedings{liu2023verilogeval,
  title={{VerilogEval:} Evaluating Large Language Models for Verilog Code Generation},
  author={Liu, Mingjie and Pinckney, Nathaniel and Khailany, Brucek and Ren, Haoxing},
  booktitle={2023 IEEE/ACM International Conference on Computer-Aided Design (ICCAD)}, 
  year={2023}
}
"""

def read_jsonl(file_name: str) -> dict:
    jsonl = dict()
    with open(file_name) as file:
        for line in file:
            current_json = json.loads(line)
            jsonl[current_json.pop("task_id")] = current_json 
    return jsonl


def create_all_tasks():
    """Creates a dictionary of tasks from both datasets."""
    return {"verilogeval": create_task(["Machine", "Human"]), 
    "verilogeval-human": create_task(["Human"]), "verilogeval-machine": create_task(["Machine"])}

def create_task(dataset_names):
    class VerilogEval(GeneralVerilogEval):
        def __init__(self, **kwargs):
            super().__init__(dataset_names, **kwargs)

    return VerilogEval

class GeneralVerilogEval(Task):
    def __init__(self, dataset_names=["Machine", "Human"], k=[1, 5, 10, 100], num_workers=32, timeout=30.0):
        """
        :param dataset_names: list(str)
            list of names of datasets for task
            ("Machine" corresponds to VerilogEval-machine dataset and "Human" to VerilogEval-human)
        :param k: list(int)
            list of ks for which we want pass@k counted
        :param num_workers: int
            max number of threads for code execution
        :param timeout: float
            time limit (in seconds) for each code execution
        """
        super().__init__(
            stop_words=["endmodule"],
            requires_execution=True
        )
        self.k = k
        self.num_workers = num_workers
        self.timeout = timeout

        self.dataset_names = dataset_names
        self.dataset = []

        # we need to merge all datasets into self.dataset, so in dataset_indices we keep track of their ranges
        # e.g. dataset_indices["Human"] consists of indices of first and last elements from "Human" in self.dataset
        self.dataset_indices = dict()

        def _load_dataset():
            for dataset_name in dataset_names:
                local_data_path = f"bigcode_eval/tasks/datasets/verilog/VerilogEval_{dataset_name}.jsonl"
                eval_set = read_jsonl(local_data_path)

                local_descriptions_path = f"bigcode_eval/tasks/datasets/verilog/VerilogDescription_{dataset_name}.jsonl"
                descriptions_set = read_jsonl(local_descriptions_path)

                self.dataset_indices[dataset_name] = (len(self.dataset), len(self.dataset) + len(eval_set))
                self.dataset += [eval_set[key] | descriptions_set[key] for key in eval_set.keys()]

        _load_dataset()

    def get_dataset(self):
        """Returns dataset for the task or an iterable of any object, that get_prompt can handle"""
        return self.dataset
    
    def get_prompt(self, doc):
        """Builds the prompt for the LM to generate from.
        :param doc: dict[str: str]
            sample from the test dataset
        """
        system_prompt = "You only complete chats with syntax correct Verilog code. "\
            "End the Verilog module code completion with 'endmodule'. "\
            "Do not include module, input and output definitions."
        question_prompt = "Implement the Verilog module based on the following description. "\
            "Assume that signals are positive clock/clk edge triggered unless otherwise stated."
        return system_prompt + "\n" + question_prompt + "\n" + doc["detail_description"] + "\n" + doc["prompt"]
    
    def get_reference(self, doc):
        """Builds the reference solution for the doc.
        :param doc: dict[str: str]
            sample from the test dataset
        """
        return doc["test"]
    
    def postprocess_generation(self, generation, idx):
        """Defines the postprocessing for a LM generation.
        :param generation: str
            code generation from LM
        :param idx: int
            index of doc in the dataset to which the generation belongs
        """
        prompt = self.get_prompt(self.dataset[idx])
        generation = generation[len(prompt) :]
        return self.dataset[idx]["prompt"] + self._stop_at_stop_token(generation, self.stop_words) + "endmodule"

    def process_results(self, generations, references):
        """Takes the list of LM generations and evaluates them against ground truth references,
        returning the metric for the generations as in {"metric_name": result}.
        :param generations: list(list(str))
            list of lists containing generations
        :param references: list(str)
            list of str containing references
        :return: dict[str: float]
        """
        results = dict()

        for dataset_name in self.dataset_names:
            first = self.dataset_indices[dataset_name][0]
            last = self.dataset_indices[dataset_name][1]
            if first >= len(generations):
                warnings.warn(f"At least one dataset was skipped (--limit parameter may be too small)")
                break

            dataset_results, _ = compute_code_eval(
                references=references[first:last],
                predictions=generations[first:last],
                k=self.k,
                num_workers=self.num_workers,
                timeout=self.timeout,
                correctness_func=verilog_correctness
            )

            results |= {f"{dataset_name}_{key}":value for key, value in dataset_results.items()}

        return results