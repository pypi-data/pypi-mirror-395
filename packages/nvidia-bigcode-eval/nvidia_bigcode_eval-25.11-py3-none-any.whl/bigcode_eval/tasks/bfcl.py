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
Homepage: https://gorilla.cs.berkeley.edu/blogs/8_berkeley_function_calling_leaderboard.html
GH: https://github.com/ShishirPatil/gorilla/tree/main/berkeley-function-call-leaderboard
"""

from ast import literal_eval
import json
import logging
import re
import random
from typing import List, Literal, Optional

from datasets import load_dataset

from bigcode_eval.base import Task
from bigcode_eval.tasks.custom_metrics.bfcl_metrics.evaluation import single_ast_file_runner
from bigcode_eval.tasks.custom_metrics.bfcl_metrics.utils import  func_doc_language_specific_pre_processing, convert_to_tool, system_prompt_pre_processing_chat_model
from bigcode_eval.tasks.custom_metrics.bfcl_metrics.constant import (
    TEST_FILE_MAPPING,
    DEFAULT_SYSTEM_PROMPT,
    GORILLA_TO_OPENAPI
)

from bigcode_eval.tasks.custom_metrics.bfcl_metrics.model_style import ModelStyle
from bigcode_eval.server.schemas import OpenAiChatCompletionParams, OpenAiOutputWithTools

from bigcode_eval.tasks.custom_metrics.bfcl_metrics.evaluation import (
    single_ast_file_runner,
)



_CITATION = """
@inproceedings{berkeley-function-calling-leaderboard,
  title={Berkeley Function Calling Leaderboard},
  author={Fanjia Yan and Huanzhi Mao and Charlie Cheng-Jie Ji and Tianjun Zhang and Shishir G. Patil and Ion Stoica and Joseph E. Gonzalez},
  year={2024},
  howpublished={\\url{https://gorilla.cs.berkeley.edu/blogs/8_berkeley_function_calling_leaderboard.html}},
}
"""

AST = [
    "simple",
    "parallel",
    "multiple",
    "parallel_multiple",
    "java",
    "javascript",
    "live_simple",
    "live_multiple",
    "live_parallel",
    "live_parallel_multiple",
]

EXECUTABLE = [
    "executable_simple",
    "executable_multiple_function",
    "executable_parallel_function",
    "executable_parallel_multiple_function",
    "rest",
]


def create_all_tasks():
    """Creates a dictionary of tasks from a list of levels
    :return: {task_name: task}
        e.g. {multiple-py: Task, multiple-java: Task}
    """
    return {"bfcl-ast": BFCLAST, "bfcl-executable": BFCLExec}


def dict_to_function_call(function_call_list):
    if type(function_call_list) == dict:
        function_call_list = [function_call_list]
    execution_list = []
    for function_call in function_call_list:
        for key, value in function_call.items():
            execution_list.append(
                f"{key}({','.join([f'{k}={repr(v)}' for k,v in value.items()])})"
            )
    return execution_list


def extract_function_calls(generation: str, function_name: str) -> list[str]:
    """
    Extracts Python-like function calls from a string.

    Assumptions:
        * The function call format is `<FUNCTION NAME>(...)`.
        * The arguments of the function may contain parentheses `(` and `)`, representing either
          data structures like tuples or string characters.
        * If `(` or `)` is used as part of a data structure, the parentheses must be balanced.
        * If `(` or `)` is used as a string character, it must be properly quoted.
        * It can handle multiple occurrences of the same function in the string.


    Args:
        generation (str): The input string containing function calls.
        function_name (str): The name of the function to extract.

    Returns:
        list[str]: A list of extracted function calls, including their arguments.

    Examples:
        The following examples demonstrate the different cases this function can handle:

        >>> extract_function_calls("foo(1,2)", "foo")
        ['foo(1,2)']
        # Simple function call without any nesting or complex structures.

        >>> extract_function_calls("foo(1, ((2, 3)))", "foo")
        ['foo(1, ((2, 3)))']
        # The function call includes nested parentheses.

        >>> extract_function_calls("Hi, foo(1, (2, 3))", "foo")
        ['foo(1, (2, 3))']
        # The function call is extracted from a string with additional text.

        >>> extract_function_calls("foo(1, ' ) ')", "foo")
        ["foo(1, ' ) ')"]
        # Parentheses are used inside a string argument and are properly quoted.

        >>> extract_function_calls("foo(1, ", "foo")
        []
        # Incomplete function calls, where the parentheses are not balanced, are ignored.

        >>> extract_function_calls("foo(1) and foo(2)", "foo")
        ['foo(1)', 'foo(2)']
        # Multiple function calls are extracted when they appear in the same string.
    """    
    # Regular expression to find all occurrences of function_name(
    pattern = rf"\b{re.escape(function_name)}\("

    # Find all positions where function_name( occurs
    matches = [match.start() for match in re.finditer(pattern, generation)]

    # List to store the extracted function calls
    function_calls = []

    # Extract the full function calls
    for start in matches:
        open_parens = 0
        in_single_quote = False
        in_double_quote = False

        for i in range(start, len(generation)):
            char = generation[i]

            # Toggle flags for single or double quotes
            if char == "'" and not in_double_quote:
                in_single_quote = not in_single_quote
            elif char == '"' and not in_single_quote:
                in_double_quote = not in_double_quote

            # Count parentheses only when not inside quotes
            if char == "(" and not in_single_quote and not in_double_quote:
                open_parens += 1
            elif char == ")" and not in_single_quote and not in_double_quote:
                open_parens -= 1

                # When parentheses are balanced, extract the function call
                if open_parens == 0:
                    function_calls.append(generation[start: i + 1])
                    break

    return function_calls



def parse_hf_tools(response: str, html_tag='tool_call') -> List[dict]:
    from bs4 import BeautifulSoup
    calls = []
    soup = BeautifulSoup(response, 'html.parser')
    for tool_call_tag in soup.find_all(html_tag):
        print('tag')
        tool_call_str = tool_call_tag.get_text(strip=True)
        try:
            # Convert the JSON string to a dictionary
            tool_call_dict = json.loads(tool_call_str)
            calls.append({tool_call_dict['name']: tool_call_dict['arguments']})
        except:
            logging.debug(f"Failed to decode: {tool_call_str}")
    return calls


def parse_mistral_tools(response: str) -> List[dict]:
    prefix = '[TOOL_CALLS]'
    calls = []
    if response.startswith(prefix):
        tool_call_str = response[len(prefix):]
        try:
            tool_call_dicts = json.loads(tool_call_str)
            calls = [{tool_call_dict['name']: tool_call_dict['arguments']} for tool_call_dict in tool_call_dicts]
        except:
            logging.debug(f"Failed to decode: {tool_call_str}")
    return calls


def parse_llama_tools(response: str) -> List[dict]:
    prefix = '<|python_tag|>'
    suffix = '<|eom_id|>'
    calls = []
    if response.startswith(prefix):
        tool_call_str = response[len(prefix):]
        if response.endswith(suffix):
            tool_call_str = tool_call_str[:-len(suffix)]
        try:
            tool_call_dicts = [literal_eval(single_tool_str) for single_tool_str in tool_call_str.split(';')]
            calls = [{tool_call_dict['name']: tool_call_dict['parameters']} for tool_call_dict in tool_call_dicts]
        except:
            logging.debug(f"Failed to decode: {tool_call_str}")
    return calls


TOOLS_PARSERS = {
    "hf": parse_hf_tools,
    "mistral": parse_mistral_tools,
    "llama": parse_llama_tools,
}


class BFCL(Task):
    DATASET_NAME = None

    BASE_DATASET_LINK = "https://huggingface.co/datasets/gorilla-llm/Berkeley-Function-Calling-Leaderboard/resolve/main/"

    TEST_CATEGORY_KEY = "test_category"
    ANSWER_KEY = "answer"
    ID_KEY = "id"

    TEST_NAMES = None  # List of test categories, set in subclass
    model_style = ModelStyle.OpenAI

    def __init__(
        self,
        stop_words=None,
        requires_execution=True,
        system_role_supported: bool = True,
        mode: Literal["original", "relaxed", "openai"] = "relaxed",
        tools_format: Literal["hf", "mistral", "llama"] = "hf",
    ):
        """
        :param stop_words: list
            list of stop words if the generation uses a stopping criteria during generation
        :param requires_execution: bool
            wheter the task requires code execution during evaluation or not
        :param support_system_role: bool
            whether to return the first message with the 'system' role unchanged, or merge
            it with the first 'user' message.
        :param mode: Literal["original", "relaxed", "openai"]
            mode of prompt and gneeration processing. "original" uses chat and original
            postprocessing of the BFCL benchmark. "relaxed" uses chat and extracts the
            relevant function calls from the model response. "openai" uses the tool
            calling API instead of using the functions in text chat
        :param tools_format: Literal["hf", "mistral", "llama"]
            which parser to use in function postprocessing in the "openai" mode
        """
        super().__init__(stop_words=stop_words, requires_execution=requires_execution)
        self.system_role_supported = system_role_supported
        self.mode = mode
        if tools_format not in TOOLS_PARSERS:
            raise ValueError(f"Unknown tools_format: {tools_format}, please provide one of: {list(TOOLS_PARSERS)}")
        self.tool_parser = TOOLS_PARSERS[tools_format]

    @staticmethod
    def remove_sys_role(messages):
        if messages[0]["role"] == "system":
            if len(messages) == 1: # Some prompts in the dataset have only system prompt with question
                messages[0]["role"] = "user"
                return messages

            sys_msg, first_msg, *remaining = messages
            first_msg = {
                "role": "user",
                "content": sys_msg["content"] + "\n" + first_msg["content"],
            }
            messages = [first_msg] + remaining
        return messages

    def _get_task_jsons(self, test_category):
        task_file = TEST_FILE_MAPPING[test_category]
        task_hf_link = self.BASE_DATASET_LINK + task_file
        dataset = load_dataset("text", data_files=task_hf_link, split="train")
        task_jsons = [json.loads(datapoint["text"]) for datapoint in dataset]
        return task_jsons

    def _get_possible_answers(self, test_category):
        possible_answer_file = TEST_FILE_MAPPING[test_category]
        possible_answer_hf_link = (
            self.BASE_DATASET_LINK + "possible_answer/" + possible_answer_file
        )
        dataset = load_dataset(
            "text", data_files=possible_answer_hf_link, split="train"
        )
        possible_answer_jsons = [json.loads(datapoint["text"]) for datapoint in dataset]
        possible_answers = {answer[self.ID_KEY]: answer["ground_truth"] for answer in possible_answer_jsons}
        return possible_answers

    def _load_dataset(self, sample_size: Optional[float] = 0, seed: Optional[int] = None):
        if sample_size is not None:
            random.seed(seed)
        dataset_jsons = []

        for test_category in self.TEST_NAMES:
            task_jsons = self._get_task_jsons(test_category)
            possible_answers = self._get_possible_answers(test_category)

            assert len(task_jsons) == len(possible_answers)

            if sample_size is not None:
                task_jsons = random.sample(task_jsons, k=int(sample_size * len(task_jsons)))

            for task_json in task_jsons:
                task_id = task_json[self.ID_KEY]
                task_json[self.TEST_CATEGORY_KEY] = test_category
                task_json[self.ANSWER_KEY] = possible_answers[task_id]

            dataset_jsons.extend(task_jsons)

        self.dataset = dataset_jsons

    def get_dataset(self):
        """Returns dataset for the task or an iterable of any object, that get_prompt can handle"""
        return self.dataset

    def get_prompt(self, doc):
        """
        Builds the prompt for the LM to generate from.
        :param doc: dict[str: str]
            sample from the test dataset
        :return: str
        """
        test_category = doc[self.TEST_CATEGORY_KEY]
        question = doc["question"][0] # Index 0 works for single-turn categories
        function = doc["function"]

        functions = func_doc_language_specific_pre_processing(function, test_category)

        if not self.mode == "openai":
            prompt = system_prompt_pre_processing_chat_model(
                question, DEFAULT_SYSTEM_PROMPT, functions
            )
            if not self.system_role_supported:
                prompt = self.remove_sys_role(prompt)
            prompt = OpenAiChatCompletionParams(messages=prompt)
        else:
            oai_tool = convert_to_tool(
                functions, GORILLA_TO_OPENAPI, self.model_style, test_category
            )
            prompt = OpenAiChatCompletionParams(messages=question, tools=oai_tool)
        return prompt

    def get_reference(self, doc):
        """
        Builds the reference solution for the doc (sample from the test dataset).
        :param doc: dict[str: str]
            sample from the test dataset
        :return: str
        """
        return doc[self.ANSWER_KEY]

    def postprocess_generation(self, generation: str | OpenAiOutputWithTools, idx):
        """
        Defines the postprocessing for a LM generation.
        :param generation: str
            code generation from LM
        :param idx: int (if needed)
            index of doc in the dataset to which the generation belongs
        :return: str
        """
        if self.mode == "original":
            generation = generation.replace("\n", "")
            if len(generation) > 0 and " " == generation[0]:
                generation = generation[1:]
            if not generation.startswith("["):
                generation = "[" + generation
            if not generation.endswith("]"):
                generation = generation + "]"
            return generation

        elif self.mode == "relaxed":
            generation = generation.replace("\n", "")
            generations_list = []
            functions = (
                [self.dataset[idx]["function"]]
                if isinstance(self.dataset[idx]["function"], dict)
                else self.dataset[idx]["function"]
            )
            for function in functions:
                generations_list.extend(
                    extract_function_calls(generation, function["name"])
                )
            generation = f"[{','.join(generations_list)}]"
            return generation
        elif self.mode == "openai":
            if isinstance(generation, str):
                tools = self.tool_parser(generation)
            elif generation["tools"] is not None:
                tools = generation["tools"]
            else:
                tools = []
            decoded_output = dict_to_function_call(tools)
            return f"[{','.join(decoded_output)}]"
        else:
            raise RuntimeError(f"Unknown mode = {self.mode} during postprocessing. How did we end up here?")



class BFCLAST(BFCL):
    TEST_NAMES = AST

    def __init__(self,
        system_role_supported: bool = True,
        mode: Literal["original", "relaxed", "openai"] = "relaxed",
        tools_format: Literal["hf", "mistral", "llama"] = "hf",
        sample_size: Optional[float] = None,
        seed: Optional[int] = 0, # Default 0 for reproducible results, use null for random seed
        ):
        super().__init__(
            stop_words=["]\n"],
            requires_execution=False,
            system_role_supported=system_role_supported,
            mode=mode,
            tools_format=tools_format,
        )
        self._load_dataset(sample_size, seed)

    def process_results(self, generations, references):
        """
        Takes the list of LM generations and evaluates them against ground truth references,
        returning the metric for the generations as in {"metric_name": result}.
        We encourage to directly load the metric from `evaluate` library to keep the code concise.
        :param generations: list(list(str))
            list of lists containing generations
        :param references: list(str)
            list of str containing refrences
        :return: dict[str: float]
        """

        PLACEHOLDER_MODEL_NAME = "MODEL_NAME"
        if self.mode == "openai":
            references = [
                [
                    {re.sub(r"\.", "_", func_name): values}
                    for func_dict in ref
                    for func_name, values in func_dict.items()
                ]
                for ref in references
            ]

            new_dataset = []

            for sample in self.dataset:
                if 'function' in sample and isinstance(sample['function'], list):
                    for func in sample['function']:
                        if 'name' in func:
                            # Replace periods with underscores in 'name'
                            func['name'] = re.sub(r"\.", "_", func['name'])

                # Append the modified sample to the new dataset
                new_dataset.append(sample)
                self.dataset = new_dataset

        results = single_ast_file_runner(
            self.dataset,
            self.TEST_CATEGORY_KEY,
            generations,
            references,
            PLACEHOLDER_MODEL_NAME,
        )

        calculated_ast_metrics = [
            "summary_ast_non_live",
            "simple_ast_non_live",
            "python_simple_ast_non_live",
            "java_simple_ast_non_live",
            "javascript_simple_ast_non_live",
            "multiple_ast_non_live",
            "parallel_ast_non_live",
            "parallel_multiple_ast_non_live",
            "summary_ast_live",
            "python_simple_ast_live",
            "python_multiple_ast_live",
            "python_parallel_ast_live",
            "python_parallel_multiple_ast_live",
            "total_summary_ast",
            "total_simple_ast",
            "total_multiple_ast",
            "total_parallel_ast",
            "total_parallel_multiple_ast",
        ]

        return {
            metric: results[metric]["accuracy"] for metric in calculated_ast_metrics
        }


class BFCLExec(BFCL):
    TEST_NAMES = EXECUTABLE

    def __init__(self):
        raise NotImplementedError("BFCL in execute mode not implemented")

        super().__init__(
            stop_words=["\n"],
            requires_execution=True,
        )
