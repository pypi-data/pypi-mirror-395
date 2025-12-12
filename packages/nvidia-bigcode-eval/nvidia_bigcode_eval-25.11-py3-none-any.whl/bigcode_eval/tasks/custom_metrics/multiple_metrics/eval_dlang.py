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
import re
from pathlib import Path

from .safe_subprocess import run

ENABLE_SYNTAX_CHECK = False


def eval_script(path: Path):
    result = run(["rdmd", "-unittest", str(path)], timeout_seconds=15)
    if "might not be correctly installed" in result.stderr:
        raise Exception("D is not correctly installed")

    if result.timeout:
        status = "Timeout"
    elif result.exit_code == 0:
        status = "OK"
    elif "Error:" in result.stderr:
        status = "SyntaxError"
    else:
        status = "Exception"

    return {
        "status": status,
        "exit_code": result.exit_code,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }


DIR = "d-keep-code_davinci_001_temp_0.2"


def main():
    directory = Path(Path(__file__).parent, "..", "datasets", DIR).resolve()

    count = {"OK": 0, "Timeout": 0, "Exception": 0, "SyntaxError": 0}
    for filename in os.listdir(directory):
        path = Path.joinpath(directory, filename)
        r = eval_script(path)
        status = r["status"]
        count[status] += 1

        if ENABLE_SYNTAX_CHECK and status == "SyntaxError":
            error_msgs = r["stderr"].split("\n")
            with open(path) as source_file:
                lines = source_file.readlines()
                unittest_line_start = lines.index("unittest\n")
                unittest_line_end = len(lines)
                for err_msg_line in error_msgs:
                    matched_parts = re.match(
                        r"(\/?.*?\.[\w:]+\/.*.d)\(([0-9]+)\): Error: (.*)",
                        err_msg_line[2:-1],
                    )
                    _file, line_num = matched_parts[1], int(matched_parts[2])
                    if (
                        unittest_line_start <= line_num
                        and line_num <= unittest_line_end
                    ):
                        print("===============")
                        print(path, "contains error in unit test part")
                        print(error_msgs)
                        print("===============")

        filename = filename.split(".")[0]
        print(f"Dlang,{filename},{status}")

    print(DIR + ":" + str(count))


if __name__ == "__main__":
    main()
