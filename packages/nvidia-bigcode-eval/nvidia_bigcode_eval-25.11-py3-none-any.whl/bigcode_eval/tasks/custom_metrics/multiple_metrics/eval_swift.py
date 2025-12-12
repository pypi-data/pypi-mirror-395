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
import subprocess
from pathlib import Path

from .safe_subprocess import run


def eval_script(path: Path):
    basename = ".".join(str(path).split(".")[:-1])
    r = run(["swiftc", path, "-o", basename], timeout_seconds=45)
    if r.timeout:
        status = "Timeout"
    elif r.exit_code != 0:
        # Well, it's a compile error. May be a type error or
        # something. But, why break the set convention
        status = "SyntaxError"
    else:
        r = run([basename], timeout_seconds=5)
        if r.timeout:
            status = "Timeout"
        elif r.exit_code != 0:
            # Well, it's a panic
            status = "Exception"
        else:
            status = "OK"
        os.remove(basename)
    return {
        "status": status,
        "exit_code": r.exit_code,
        "stdout": r.stdout,
        "stderr": r.stderr,
    }
