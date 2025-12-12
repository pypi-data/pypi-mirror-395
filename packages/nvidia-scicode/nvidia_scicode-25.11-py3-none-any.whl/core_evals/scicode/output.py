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
    output_path = list((pathlib.Path(output_dir) / "scicode_results").glob('*.json'))
    assert len(output_path) == 1, f"Expected 1 output file, found {len(output_path)} ({output_path})"
    output_path = output_path[0]
    with open(output_path) as f:
        results = json.load(f)
    metrics = {}
    for metric_type in ("steps", "problems"):
        metric_name = metric_type + "_pass@1"
        metrics[metric_name] = dict(
            scores={
                metric_name: dict(
                    value=results[metric_name],
                    stats={}
                )
            }
        )

    task_results = {"metrics": metrics}
    return EvaluationResult(tasks={'scicode': task_results}, groups={'scicode': task_results})
