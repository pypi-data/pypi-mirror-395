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
Evaluates a generated Racket program (.rkt).
"""
import os
from pathlib import Path

from .safe_subprocess import run


def eval_script(path: Path):
    result = run(["racket", str(path)])

    if (
        "standard-module-name-resolver: collection not found\n  for module path: rackunit"
        in result.stderr
    ):
        print(f"Failed to run evaluation for {path}: rackunit is not installed")
        return None

    # rackunit produces exit code 0 even if tests fail.
    if len(result.stderr) > 0 or result.exit_code != 0:
        if "read-syntax" in result.stderr:
            status = "SyntaxError"
        else:
            status = "Exception"
    else:
        status = "OK"

    return {
        "status": status,
        "exit_code": result.exit_code,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }


def main():
    directory = Path(
        Path(__file__).parent, "..", "datasets", "racket-keep-code_davinci_001_temp_0.2"
    ).resolve()

    for filename in os.listdir(directory):
        r = eval_script(Path.joinpath(directory, filename))
        filename = filename.split(".")[0]
        print(f"Racket,{filename},{r['status']}")


if __name__ == "__main__":
    main()
