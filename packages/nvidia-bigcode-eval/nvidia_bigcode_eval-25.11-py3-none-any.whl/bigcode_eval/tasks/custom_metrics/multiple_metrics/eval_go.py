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

import argparse
import subprocess
from pathlib import Path
from sys import exit

from .generic_eval import main as gmain


def eval_script(path: Path):
    status = None
    stdout = None
    stderr = None
    exit_code = None
    try:
        build = subprocess.run(
            ["go", "test", path],
            timeout=30,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        stdout = build.stdout.decode("utf-8", errors="ignore")
        stderr = build.stderr.decode("utf-8", errors="ignore")
        exit_code = build.returncode
        # write to stderr just so that we can redirect stdout to a csv

        if "[setup failed]" in stdout or "[build failed]" in stdout:
            status = "SyntaxError"
        elif "FAIL" in stdout:
            status = "Exception"
        else:
            status = "OK"
    except subprocess.TimeoutExpired:
        status = "Timeout"

    return {
        "status": status,
        "exit_code": exit_code,
        "stdout": stdout,
        "stderr": stderr,
    }


if __name__ == "__main__":
    gmain(eval_script, "Go", ".go")
