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

import glob
import json
import os
import statistics
import subprocess
import re
import numpy as np
from bigcode_eval.tasks.custom_metrics.bfcl_metrics.custom_exception import (
    BadAPIStatusError,
)
from tqdm import tqdm

REST_API_GROUND_TRUTH_FILE_PATH = "api_status_check_ground_truth_REST.json"
EXECTUABLE_API_GROUND_TRUTH_FILE_PATH = "api_status_check_ground_truth_executable.json"


RED_FONT = "\033[91m"
RESET = "\033[0m"


def extract_test_category(input_string):
    pattern = r".*BFCL_v2_(\w+?)(?:_score|_result)?\.json"
    match = re.search(pattern, input_string)

    # Check if there's a match and extract the captured group
    if match:
        return match.group(1)  # the first captured group (\w+)
    else:
        raise ValueError(
            f"Could not extract the test category from the input string: {input_string}"
        )


def find_file_with_suffix(folder_path, suffix):
    json_files_pattern = os.path.join(folder_path, "*.json")
    for json_file in glob.glob(json_files_pattern):
        if extract_test_category(json_file) == suffix:
            return json_file


def is_executable(test_category):
    return "exec" in test_category or "rest" in test_category


def is_rest(test_category):
    return "rest" in test_category


def is_relevance_or_irrelevance(test_category):
    return "relevance" in test_category or "irrelevance" in test_category


def is_chatable(test_category):
    return "chatable" in test_category


def is_java(test_category):
    return "java" in test_category


def is_js(test_category):
    return "javascript" in test_category


def is_sql(test_category):
    return "sql" in test_category


def load_file(file_path):
    result = []
    with open(file_path) as f:
        file = f.readlines()
        for line in file:
            result.append(json.loads(line))
    return result


def write_list_of_dicts_to_file(filename, data, subdir=None):
    if subdir:
        # Ensure the subdirectory exists
        os.makedirs(subdir, exist_ok=True)

        # Construct the full path to the file
        filename = os.path.join(subdir, filename)

    # Write the list of dictionaries to the file in JSON format
    with open(filename, "w") as f:
        for i, entry in enumerate(data):
            json_str = json.dumps(entry)
            f.write(json_str)
            if i < len(data) - 1:
                f.write("\n")


def is_function_calling_format_output(decoded_output):
    # Ensure the output is a list of dictionaries
    if type(decoded_output) == list:
        for item in decoded_output:
            if type(item) != dict:
                return False
        return True
    return False


def is_executable_format_output(decoded_output):
    # Ensure the output is a list of strings (one or more strings)
    if type(decoded_output) == list:
        if len(decoded_output) == 0:
            return False
        for item in decoded_output:
            if type(item) != str:
                return False
        return True
    return False


def is_rest_format_output(decoded_output):
    # Ensure the output is a list of one string
    if type(decoded_output) == list:
        if len(decoded_output) == 1 and type(decoded_output[0]) == str:
            return True
    return False


def is_empty_output(decoded_output):
    # This function is a patch to the ast decoder for relevance detection
    # Sometimes the ast decoder will parse successfully, but the input doens't really have a function call
    # [], [{}], and anything that is not in function calling format is considered empty (and thus should be marked as correct)
    if not is_function_calling_format_output(decoded_output):
        return True
    if len(decoded_output) == 0:
        return True
    if len(decoded_output) == 1 and len(decoded_output[0]) == 0:
        return True


def api_status_sanity_check_rest():

    # We only need to import the executable_checker_rest in this function. So a local import is used.
    from bigcode_eval.tasks.custom_metrics.bfcl_metrics.checker import (
        executable_checker_rest,
    )

    ground_truth_dummy = load_file(REST_API_GROUND_TRUTH_FILE_PATH)

    # Use the ground truth data to make sure the API is working correctly
    command = f"cd .. ; python apply_function_credential_config.py --input-path ./eval_checker/{REST_API_GROUND_TRUTH_FILE_PATH};"
    try:
        subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as e:
        write_list_of_dicts_to_file(REST_API_GROUND_TRUTH_FILE_PATH, ground_truth_dummy)
        raise RuntimeError(e.stderr) from e

    ground_truth_replaced = load_file(REST_API_GROUND_TRUTH_FILE_PATH)
    write_list_of_dicts_to_file(REST_API_GROUND_TRUTH_FILE_PATH, ground_truth_dummy)

    correct_count = 0
    errors = []
    for idx, data in tqdm(
        enumerate(ground_truth_replaced),
        total=len(ground_truth_replaced),
        desc="API Status Test (REST)",
    ):
        status = executable_checker_rest(data["ground_truth"], idx)
        if status["valid"]:
            correct_count += 1
        else:
            errors.append((data, status))

    if correct_count != len(ground_truth_replaced):
        raise BadAPIStatusError(
            errors,
            f"{len(ground_truth_replaced) - correct_count} / {len(ground_truth_replaced)}",
        )


def api_status_sanity_check_executable():
    from checker import executable_checker_simple

    ground_truth = load_file(EXECTUABLE_API_GROUND_TRUTH_FILE_PATH)
    correct_count = 0
    errors = []
    for data in tqdm(
        ground_truth, total=len(ground_truth), desc="API Status Test (Non-REST)"
    ):
        status = executable_checker_simple(
            data["ground_truth"][0],
            data["execution_result"][0],
            data["execution_result_type"][0],
            True,
        )
        if status["valid"]:
            correct_count += 1
        else:
            errors.append((data, status))

    if correct_count != len(ground_truth):
        raise BadAPIStatusError(
            errors, f"{len(ground_truth) - correct_count} / {len(ground_truth)}"
        )


def display_api_status_error(rest_error, executable_error, display_success=False):
    if not rest_error and not executable_error:
        if display_success:
            print("🟢 All API Status Test Passed!")
        return None

    print(
        f"\n{RED_FONT}{'-' * 18} Executable Categories' Error Bounds Based on API Health Status {'-' * 18}{RESET}\n"
    )

    if rest_error:
        print(
            f"❗️ Warning: Unable to verify health of executable APIs used in executable test category (REST). Please contact API provider.\n"
        )
        print(f"{rest_error.error_rate} APIs affected:\n")
        for data, status in rest_error.errors:
            print(f"  - Test Case: {data['ground_truth']}")
            print(f"    Error Type: {status['error_type']}\n")

    if executable_error:
        print(
            f"❗️ Warning: Unable to verify health of executable APIs used in executable test categories (Non-REST). Please contact API provider.\n"
        )
        print(f"{executable_error.error_rate} APIs affected:\n")
        for data, status in executable_error.errors:
            print(f"  - Test Case: {data['ground_truth'][0]}")
            print(f"    Error Type: {status['error_type']}\n")

    print(f"{RED_FONT}{'-' * 100}\n{RESET}")


def get_executable_expected_output(prompt_file_path):
    # Before we run the evaluation, we need to add the "execution_result" field to the prompt file, using the ground truth data.
    prompt_content = load_file(prompt_file_path)
    exec_dict = {}
    for item in tqdm(prompt_content, desc="Getting Executable Expected Output"):
        execution_result = []
        ground_truth = item["ground_truth"]
        for i in range(len(ground_truth)):
            exec(
                "from executable_python_function import *"
                + "\nresult="
                + ground_truth[i],
                exec_dict,
            )
            execution_result.append(exec_dict["result"])
        item["execution_result"] = execution_result

    write_list_of_dicts_to_file(prompt_file_path, prompt_content)


def clean_up_executable_expected_output(prompt_path, categories):
    for category in categories:
        prompt_file = find_file_with_suffix(prompt_path, category)
        prompt_content = load_file(prompt_file)
        for item in prompt_content:
            del item["execution_result"]
        write_list_of_dicts_to_file(prompt_file, prompt_content)


def calculate_weighted_accuracy(accuracy_dict_list):
    total_count = 0
    total_accuracy = 0
    for accuracy_dict in accuracy_dict_list:
        total_count += accuracy_dict["total_count"]
        total_accuracy += accuracy_dict["accuracy"] * accuracy_dict["total_count"]

    if total_count == 0:
        return {"accuracy": 0, "total_count": 0}

    return {"accuracy": total_accuracy / total_count, "total_count": total_count}


def calculate_unweighted_accuracy(accuracy_dict_list):
    total_count = 0
    total_accuracy = 0
    for accuracy_dict in accuracy_dict_list:
        total_count += accuracy_dict["total_count"]
        total_accuracy += accuracy_dict["accuracy"]

    if len(accuracy_dict_list) == 0:
        return {"accuracy": 0, "total_count": 0}

    return {
        "accuracy": total_accuracy / len(accuracy_dict_list),
        "total_count": total_count,
    }


def generate_results(value):
    # Non-Live Score
    python_simple_ast_non_live = value.get("simple", {"accuracy": 0, "total_count": 0})
    python_multiple_ast_non_live = value.get(
        "multiple", {"accuracy": 0, "total_count": 0}
    )
    python_parallel_ast_non_live = value.get(
        "parallel", {"accuracy": 0, "total_count": 0}
    )
    python_parallel_multiple_ast_non_live = value.get(
        "parallel_multiple", {"accuracy": 0, "total_count": 0}
    )
    python_simple_exec_non_live = value.get(
        "exec_simple", {"accuracy": 0, "total_count": 0}
    )
    python_multiple_exec_non_live = value.get(
        "exec_multiple", {"accuracy": 0, "total_count": 0}
    )
    python_parallel_exec_non_live = value.get(
        "exec_parallel", {"accuracy": 0, "total_count": 0}
    )
    python_parallel_multiple_exec_non_live = value.get(
        "exec_parallel_multiple", {"accuracy": 0, "total_count": 0}
    )
    java_simple_ast_non_live = value.get("java", {"accuracy": 0, "total_count": 0})
    javascript_simple_ast_non_live = value.get(
        "javascript", {"accuracy": 0, "total_count": 0}
    )
    rest_simple_exec_non_live = value.get("rest", {"accuracy": 0, "total_count": 0})
    irrelevance_non_live = value.get("irrelevance", {"accuracy": 0, "total_count": 0})

    simple_ast_non_live = calculate_unweighted_accuracy(
        [
            python_simple_ast_non_live,
            java_simple_ast_non_live,
            javascript_simple_ast_non_live,
        ]
    )
    multiple_ast_non_live = python_multiple_ast_non_live
    parallel_ast_non_live = python_parallel_ast_non_live
    parallel_multiple_ast_non_live = python_parallel_multiple_ast_non_live
    simple_exec_non_live = calculate_unweighted_accuracy(
        [python_simple_exec_non_live, rest_simple_exec_non_live]
    )
    multiple_exec_non_live = python_multiple_exec_non_live
    parallel_exec_non_live = python_parallel_exec_non_live
    parallel_multiple_exec_non_live = python_parallel_multiple_exec_non_live

    summary_ast_non_live = calculate_unweighted_accuracy(
        [
            simple_ast_non_live,
            multiple_ast_non_live,
            parallel_ast_non_live,
            parallel_multiple_ast_non_live,
        ]
    )
    summary_exec_non_live = calculate_unweighted_accuracy(
        [
            simple_exec_non_live,
            multiple_exec_non_live,
            parallel_exec_non_live,
            parallel_multiple_exec_non_live,
        ]
    )
    overall_accuracy_non_live = calculate_unweighted_accuracy(
        [
            simple_ast_non_live,
            multiple_ast_non_live,
            parallel_ast_non_live,
            parallel_multiple_ast_non_live,
            simple_exec_non_live,
            multiple_exec_non_live,
            parallel_exec_non_live,
            parallel_multiple_exec_non_live,
            irrelevance_non_live,
        ]
    )

    # Live Score
    python_simple_ast_live = value.get("live_simple", {"accuracy": 0, "total_count": 0})
    python_multiple_ast_live = value.get(
        "live_multiple", {"accuracy": 0, "total_count": 0}
    )
    python_parallel_ast_live = value.get(
        "live_parallel", {"accuracy": 0, "total_count": 0}
    )
    python_parallel_multiple_ast_live = value.get(
        "live_parallel_multiple", {"accuracy": 0, "total_count": 0}
    )
    irrelevance_live = value.get("live_irrelevance", {"accuracy": 0, "total_count": 0})
    relevance_live = value.get("live_relevance", {"accuracy": 0, "total_count": 0})
    summary_ast_live = calculate_weighted_accuracy(
        [
            python_simple_ast_live,
            python_multiple_ast_live,
            python_parallel_ast_live,
            python_parallel_multiple_ast_live,
        ]
    )

    overall_accuracy_live = calculate_weighted_accuracy(
        [
            python_simple_ast_live,
            python_multiple_ast_live,
            python_parallel_ast_live,
            python_parallel_multiple_ast_live,
            irrelevance_live,
            relevance_live,
        ]
    )

    # Total Score
    total_simple_ast = calculate_unweighted_accuracy(
        [simple_ast_non_live, python_simple_ast_live]
    )
    total_multiple_ast = calculate_unweighted_accuracy(
        [multiple_ast_non_live, python_multiple_ast_live]
    )
    total_parallel_ast = calculate_unweighted_accuracy(
        [parallel_ast_non_live, python_parallel_ast_live]
    )
    total_parallel_multiple_ast = calculate_unweighted_accuracy(
        [parallel_multiple_ast_non_live, python_parallel_multiple_ast_live]
    )
    total_simple_exec = simple_exec_non_live
    total_multiple_exec = multiple_exec_non_live
    total_parallel_exec = parallel_exec_non_live
    total_parallel_multiple_exec = parallel_multiple_exec_non_live
    total_irrelevance = calculate_unweighted_accuracy(
        [irrelevance_non_live, irrelevance_live]
    )
    total_relevance = relevance_live

    total_summary_ast = calculate_unweighted_accuracy(
        [
            total_simple_ast,
            total_multiple_ast,
            total_parallel_ast,
            total_parallel_multiple_ast,
        ]
    )
    total_summary_exec = calculate_unweighted_accuracy(
        [
            total_simple_exec,
            total_multiple_exec,
            total_parallel_exec,
            total_parallel_multiple_exec,
        ]
    )
    total_overall_accuracy = calculate_unweighted_accuracy(
        [
            total_simple_ast,
            total_multiple_ast,
            total_parallel_ast,
            total_parallel_multiple_ast,
            total_simple_exec,
            total_multiple_exec,
            total_parallel_exec,
            total_parallel_multiple_exec,
            total_irrelevance,
            total_relevance,
        ]
    )

    return {
        "overall_accuracy_non_live": overall_accuracy_non_live,
        "summary_ast_non_live": summary_ast_non_live,
        "summary_exec_non_live": summary_exec_non_live,
        "simple_ast_non_live": simple_ast_non_live,
        "python_simple_ast_non_live": python_simple_ast_non_live,
        "java_simple_ast_non_live": java_simple_ast_non_live,
        "javascript_simple_ast_non_live": javascript_simple_ast_non_live,
        "multiple_ast_non_live": multiple_ast_non_live,
        "parallel_ast_non_live": parallel_ast_non_live,
        "parallel_multiple_ast_non_live": parallel_multiple_ast_non_live,
        "simple_exec_non_live": simple_exec_non_live,
        "python_simple_exec_non_live": python_simple_exec_non_live,
        "rest_simple_exec_non_live": rest_simple_exec_non_live,
        "multiple_exec_non_live": multiple_exec_non_live,
        "parallel_exec_non_live": parallel_exec_non_live,
        "parallel_multiple_exec_non_live": parallel_multiple_exec_non_live,
        "irrelevance_non_live": irrelevance_non_live,
        "overall_accuracy_live": overall_accuracy_live,
        "summary_ast_live": summary_ast_live,
        "python_simple_ast_live": python_simple_ast_live,
        "python_multiple_ast_live": python_multiple_ast_live,
        "python_parallel_ast_live": python_parallel_ast_live,
        "python_parallel_multiple_ast_live": python_parallel_multiple_ast_live,
        "irrelevance_live": irrelevance_live,
        "relevance_live": relevance_live,
        "total_overall_accuracy": total_overall_accuracy,
        "total_summary_ast": total_summary_ast,
        "total_summary_exec": total_summary_exec,
        "total_simple_ast": total_simple_ast,
        "total_multiple_ast": total_multiple_ast,
        "total_parallel_ast": total_parallel_ast,
        "total_parallel_multiple_ast": total_parallel_multiple_ast,
        "total_simple_exec": total_simple_exec,
        "total_multiple_exec": total_multiple_exec,
        "total_parallel_exec": total_parallel_exec,
        "total_parallel_multiple_exec": total_parallel_multiple_exec,
        "total_irrelevance": total_irrelevance,
        "total_relevance": total_relevance,
    }
