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


def eval_script(path: Path):
    result = run(["julia", str(path)], timeout_seconds=5)
    if result.timeout:
        status = "Timeout"
    elif result.exit_code == 0:
        status = "OK"
    # TODO(arjun): I would like this to be reviewed more carefully by John.
    elif len(result.stderr) < 1:
        status = "Exception"
    else:
        status = "SyntaxError"

    return {
        "status": status,
        "exit_code": result.exit_code,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }
