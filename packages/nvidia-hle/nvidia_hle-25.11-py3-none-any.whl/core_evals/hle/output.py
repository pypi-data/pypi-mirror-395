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
    results_files = list(pathlib.Path(output_dir).rglob("**/results_hle*.json"))
    if not results_files:
        raise FileNotFoundError("Failed to find a results file.")
    if len(results_files) > 1:
        raise ValueError(
            "More than 1 results file found. `output_dir` must contain a single evaluation"
        )
    with open(results_files[0]) as fp:
        results = json.load(fp)
    
    results_dict = results['results']['accuracy']
    tasks = {
        "hle": dict(
            metrics={
                "accuracy": dict(
                    scores={
                        "accuracy": dict(
                            value=results_dict["value"],
                            stats={},
                        ),
                        **{
                            name: dict(value=stat, stats={})
                            for name, stat in results_dict['stats'].items()
                            if stat is not None
                        }
                    }
                )
            }
        )
    }
    return EvaluationResult(tasks=tasks, groups=tasks)  # no subtasks

