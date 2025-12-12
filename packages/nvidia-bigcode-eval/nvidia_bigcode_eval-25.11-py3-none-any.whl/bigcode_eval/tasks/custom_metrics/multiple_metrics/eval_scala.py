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

import tempfile
from pathlib import Path

from .safe_subprocess import run

LANG_NAME = "Scala"
LANG_EXT = ".scala"


def eval_script(path: Path):
    with tempfile.TemporaryDirectory() as outdir:
        # Each Scala file contains the class with same name `JAVA_CLASS_NAME`
        # Hence, scalac will same JAVA_CLASS_NAME.class file for each problem
        # Write class for each problem to a different temp dir
        build = run(["scalac", "-d", outdir, path], timeout_seconds=45)
        if build.exit_code != 0:
            # Well, it's a compile error. May be a type error or
            # something. But, why break the set convention
            return {
                "status": "SyntaxError",
                "exit_code": build.exit_code,
                "stdout": build.stdout,
                "stderr": build.stderr,
            }
        # "Problem" is the name of the class we emit.
        r = run(["scala", "-cp", f"{outdir}", "Problem"])
        if r.timeout:
            status = "Timeout"
        elif r.exit_code == 0 and r.stderr == "":
            status = "OK"
        else:
            # Well, it's a panic
            status = "Exception"
    return {
        "status": status,
        "exit_code": r.exit_code,
        "stdout": r.stdout,
        "stderr": r.stderr,
    }
