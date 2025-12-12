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

import pathlib
import json
from nemo_evaluator.api.api_dataclasses import EvaluationResult


def parse_output(output_dir: str) -> EvaluationResult:
    result_files = list(pathlib.Path(output_dir).rglob("*_genai_perf.json"))
    if not result_files:
        raise FileNotFoundError("Failed to find results json.")
    if len(result_files) > 1:
        raise ValueError(
            "More than 1 results json files found. `output_dir` must contain a single evaluation."
        )
    # load the json file
    with open(result_files[0], "r") as f:
        results = json.load(f)

    stats = ["avg", "min", "max", "std", "p25", "p50", "p75", "p90", "p95", "p99"]
    metric_names = [
        "request_throughput", "request_latency", "time_to_first_token", "inter_token_latency",
        "output_token_throughput", "output_token_throughput_per_request",
        "output_sequence_length", "input_sequence_length",
    ] 

    metrics = {
        metric_name: {
            "scores": {
                stat_name: {
                    "value": results[metric_name][stat_name],
                    "stats": {},
                } for stat_name in stats if stat_name in results[metric_name]
            }
        } for metric_name in metric_names if metric_name in results
    }

    tasks = {
        "genai_perf": dict(
            metrics=metrics,
        )
    }

    return EvaluationResult(tasks=tasks, groups=tasks)

