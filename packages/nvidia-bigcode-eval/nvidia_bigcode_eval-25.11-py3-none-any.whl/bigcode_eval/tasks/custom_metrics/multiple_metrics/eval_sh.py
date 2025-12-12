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

from pathlib import Path

from .safe_subprocess import run

LANG_NAME = "bash"
LANG_EXT = ".sh"


def eval_script(path: Path):
    # Capture output - will be generated regardless of success, fail, or syntax error
    p = run(["bash", path])
    if p.timeout:
        status = "Timeout"
    elif p.exit_code == 0:
        status = "OK"
    elif "syntax error" in p.stderr:
        status = "SyntaxError"
    else:
        status = "Exception"

    return {
        "status": status,
        "exit_code": p.exit_code,
        "stdout": p.stdout,
        "stderr": p.stderr,
    }
