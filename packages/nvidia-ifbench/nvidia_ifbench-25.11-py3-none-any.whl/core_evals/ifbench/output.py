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
from nemo_evaluator.api.api_dataclasses import EvaluationResult, TaskResult, MetricResult, Score

def parse_output(output_dir):

    metrics_file = os.path.join(output_dir, 'metrics.json')
    with open(metrics_file, 'r') as file:
        metrics = json.load(file)
    tasks = {}

    metrics_transformed = {
        metric : MetricResult(
            scores={
                metric: Score(
                    value=value,
                    stats={},
                )
            }
    ) for metric, value in metrics.items() }

    tasks["ifbench"] = TaskResult(
            metrics=metrics_transformed
        )
    return EvaluationResult(groups=None, tasks=tasks)
