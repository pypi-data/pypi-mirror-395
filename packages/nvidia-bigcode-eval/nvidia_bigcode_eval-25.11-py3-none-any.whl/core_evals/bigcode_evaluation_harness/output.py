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

import json
import pathlib

from nemo_evaluator.api.api_dataclasses import EvaluationResult



def parse_output(output_dir: str) -> EvaluationResult:
    metrics_filepath = pathlib.Path(output_dir) / "metrics.json"
    if not metrics_filepath.exists():
        raise FileNotFoundError("Failed to find `metrics.json`.")
    with open(metrics_filepath) as fp:
        results = json.load(fp)
    del results["config"]

    tasks = {}
    for task_name, task_metrics in results.items():
        metrics = {}
        for metric_name, metric_value in task_metrics.items():
            if "stderr" in metric_name:
                continue
            stderr_name = f"{metric_name}_stderr"
            stats = {}
            if stderr_name in task_metrics:
                stats["stderr"] = task_metrics[stderr_name]
            metric_result = dict(
                scores={
                    metric_name: dict(value=metric_value, stats=stats)
                }
            )
            metrics[metric_name] = metric_result
        task_result = dict(metrics=metrics)
        tasks[task_name] = task_result
    evaluation_result = EvaluationResult(
        tasks=tasks,
        groups=tasks  # NOTE(dfridman): currently no support for aggregated metrics (e.g. Multipl-E)
    )
    return evaluation_result
