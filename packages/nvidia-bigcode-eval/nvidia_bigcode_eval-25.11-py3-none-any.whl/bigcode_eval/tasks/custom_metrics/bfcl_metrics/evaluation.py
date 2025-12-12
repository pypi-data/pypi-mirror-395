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

from collections import defaultdict
import re

from bigcode_eval.tasks.custom_metrics.bfcl_metrics.checker import ast_checker
from bigcode_eval.tasks.custom_metrics.bfcl_metrics.utils import get_language, ast_parse
from bigcode_eval.tasks.custom_metrics.bfcl_metrics.eval_runner_helper import generate_results


def is_function_calling_format_output(decoded_output):
    # Ensure the output is a list of dictionaries
    if type(decoded_output) == list:
        for item in decoded_output:
            if type(item) != dict:
                return False
        return True
    return False


def single_ast_file_runner(
    dataset,
    test_category_key,
    model_result,
    possible_answer,
    model_name,
):
    correct_count = defaultdict(int)
    total_count = defaultdict(int)

    for i in range(len(model_result)):
        model_result_item = model_result[i][0]
        possible_answer_item = possible_answer[i]

        prompt_item = dataset[i]["function"]
        test_category = dataset[i][test_category_key]
        language = get_language(test_category)

        total_count[test_category] += 1
        try:
            decode_output = ast_parse(model_result_item, language)
            model_result_item = decode_output

        except Exception as e:
            # Error in parsing, not a correct model response
            continue

        decoder_output_valid = is_function_calling_format_output(model_result_item)
        if not decoder_output_valid:
            continue

        checker_result = ast_checker(
            prompt_item,
            model_result_item,
            possible_answer_item,
            language,
            test_category,
            model_name,
        )
        if checker_result["valid"]:
            correct_count[test_category] += 1

    accuracy_result = {
        test_category: {
            "correct_count": correct_count[test_category],
            "total_count": total_count[test_category],
            "accuracy": correct_count[test_category] / total_count[test_category],
            } for test_category in correct_count.keys()
    }

    results = generate_results(accuracy_result)

    return results
