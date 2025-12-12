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

from .generic_eval import main

LANG_NAME = "CSharp"
LANG_EXT = ".cs"

# Following files have problems:
# 137,
# 22: Any
# 148: Elipsis


def eval_script(path: str):
    if ".cs" not in path.name:
        return
    basename = ".".join(str(path).split(".")[:-1])
    binaryname = basename + ".exe"
    build = subprocess.run(
        ["csc", "/d:DEBUG", "-r:System.Numerics.dll", path, f"/out:{binaryname}"],
        capture_output=True,
    )
    status = None
    returncode = -1
    output = None
    if build.returncode != 0:
        # Well, it's a compile error. May be a type error or
        # something. But, why break the set convention
        status = "SyntaxError"
        returncode = build.returncode
        output = build
    else:
        try:
            output = subprocess.run(
                ["mono", binaryname],
                env={"PATH": os.getenv("PATH"), "MONO_TRACE_LISTENER": "Console.Error"},
                capture_output=True,
                timeout=5,
            )
            returncode = output.returncode
            output.stderr = str(output.stderr, "utf-8")
            # mono return 0 even when failing
            fail = (
                "System.Diagnostics.DefaultTraceListener.Fail" in output.stderr
                or "Unhandled Exception" in output.stderr
            )
            output.returncode = 1 if fail else 0
            if output.returncode == 0:
                status = "OK"
            else:
                # Well, it's a panic
                status = "Exception"
        except subprocess.TimeoutExpired as exc:
            status = "Timeout"
            output = exc
        os.remove(binaryname)

    if output.stdout is not None:
        output.stdout = output.stdout.decode("utf-8")
    else:
        output.stdout = "None"

    if output.stderr == "":
        output.stderr = "None"

    return {
        "status": status,
        "exit_code": returncode,
        "stdout": output.stdout,
        "stderr": output.stderr,
    }


if __name__ == "__main__":
    main(eval_script, LANG_NAME, LANG_EXT)
