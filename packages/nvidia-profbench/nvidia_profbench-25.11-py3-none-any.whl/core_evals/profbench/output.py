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
    """
    Parse ProfBench evaluation output.
    
    This function looks for *_eval.json files created by the scoring scripts.
    """
    result_files = list(pathlib.Path(output_dir).rglob("*_eval.json"))
    if not result_files:
        raise FileNotFoundError(f"Failed to find `*_eval.json` with metrics in {output_dir}.")
    if len(result_files) > 1:
        raise ValueError(
            f"More than 1 `*_eval.json` files found in {output_dir}. `output_dir` must contain a single evaluation."
        )
    
    result_file = result_files[0]
    
    # Determine task name from filename
    if "llm_judge_eval" in result_file.name:
        task_name = "llm_judge"
    elif "report_generation_eval" in result_file.name:
        task_name = "report_generation"
    else:
        task_name = "profbench"
    
    with open(result_file) as fp:
        results = json.load(fp)
    
    # Remove detail if present
    if 'detail' in results:
        results.pop('detail')
    
    tasks = {}
    metrics = {}
    
    for metric_name, value in results.items():
        # Skip _stderr fields as they are handled with their corresponding metrics
        if metric_name.endswith("_stderr"):
            continue
        
        # Check if there's a corresponding _stderr field
        stderr_key = f"{metric_name}_stderr"
        if stderr_key in results:
            metrics[metric_name] = dict(
                scores={metric_name: dict(value=value, stats={"stderr": results[stderr_key]})}
            )
        else:
            # Provide empty stats dict as required by EvaluationResult
            metrics[metric_name] = dict(
                scores={metric_name: dict(value=value, stats={})}
            )
    
    tasks[task_name] = dict(
        metrics=metrics
    )
    return EvaluationResult(groups=tasks, tasks=tasks)
