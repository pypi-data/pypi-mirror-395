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
import json
import pathlib
import re
from typing import Dict

from nemo_evaluator.api.api_dataclasses import EvaluationResult, MetricResult, Score



# This is the only required function
def parse_output(output_dir: str) -> EvaluationResult:
    result_files = list(pathlib.Path(output_dir).rglob("results*.json"))
    latest_file = max(result_files, key=os.path.getctime, default=None)
    if latest_file is None:
        raise FileNotFoundError(
            "Failed to find results file for lm-evaluation-harness."
        )
    
    with open(latest_file) as fp:
        results = json.load(fp)
    
    groups = {
        group_name: dict(metrics=_parse_task_result(group_results))
        for group_name, group_results in results.get("groups", {}).items()
    }
    tasks = {
        task_name: dict(metrics=_parse_task_result(task_results))
        for task_name, task_results in results.get("results", {}).items()
        if task_name not in set(groups.keys())
    }
    if not groups:
        # for monolith tasks, treat them as both a task and a group
        groups = tasks
    return EvaluationResult(
        tasks=tasks,
        groups=groups,
    )


def _parse_task_result(results_dict: dict) -> Dict[str, MetricResult]:
    metric_name_pattern = "(.*),(.*)"
    metrics = {}
    for full_metric_name, metric_value in results_dict.items():
        m = re.match(metric_name_pattern, full_metric_name)
        if m is None or "stderr" in full_metric_name:
            # not a metric name
            continue
        metric_name, metric_type = m.group(1), m.group(2)
        if metric_type == "none":
            # e.g. exclude "none" from "exact_match,none"
            full_metric_name = metric_name
        normalized_metric_name = full_metric_name.replace(",", "__")
        stderr_name = f"{metric_name}_stderr,{metric_type}"
        stats = {}
        if stderr_name in results_dict:
            stderr_val = results_dict[stderr_name]
            if stderr_val == "N/A":
                stderr_val = None
            stats["stderr"] = stderr_val
        score = Score(
            value=metric_value,
            stats=stats,
        )
        metric_result = MetricResult(
            scores={normalized_metric_name: score},
        )
        metrics[normalized_metric_name] = metric_result
    return metrics
