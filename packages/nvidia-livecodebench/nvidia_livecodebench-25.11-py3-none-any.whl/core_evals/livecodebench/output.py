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
import re

from nemo_evaluator.api.api_dataclasses import EvaluationResult

# This is the only required function
def parse_output(output_dir: str) -> EvaluationResult:
    result_files = list(pathlib.Path(output_dir).rglob("*eval.json"))
    if not result_files:
        raise FileNotFoundError("Failed to find `*eval.json` with metric.")
    if len(result_files) > 1:
        raise ValueError(
            "More than 1 `*eval.json.json` files found. `output_dir` must contain a single evaluation."
        )
    match = re.search(r"Scenario\.([^_]+)_", str(result_files[0]))
    task_name = match.group(1)

    with open(result_files[0]) as fp:
        results = json.load(fp)[0]
    if 'detail' in results:
        results.pop('detail')


    tasks = {}
    metrics = {}
    for metric_name, value in results.items():
        if metric_name.endswith("_stderr"):
            continue
        metrics[metric_name] = dict(
                scores={metric_name: dict(value=value, stats={"stderr": results[f"{metric_name}_stderr"]})}
            )
    tasks[task_name] = dict(
        metrics=metrics
    )
    return EvaluationResult(groups=tasks, tasks=tasks)
