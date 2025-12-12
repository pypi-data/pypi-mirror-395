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
import yaml

from nemo_evaluator.api.api_dataclasses import EvaluationResult, TaskResult, MetricResult, Score, GroupResult

def parse_output(output_dir):

    with open(os.path.join(output_dir, "run_config.yml")) as stream:
        results_yml = yaml.safe_load(stream)
        language = results_yml['config']['params']['extra']['language']
        model_name = results_yml['target']['api_endpoint']['model_id']
    
    with open(os.path.join(output_dir, model_name, f"metrics_{language}.json"), 'r') as fp:
        metrics = json.load(fp)
    tasks = {
        subdataset : TaskResult(
            metrics={
                'accuracy': MetricResult(
                    scores={
                        'accuracy': Score(
                            value=metrics[subdataset],
                            stats={},
                        )
                    }
                ) 
            }
        ) 
       
    for subdataset in ['AIME2024', 'AIME2025', 'CNMO', 'MATH500'] 
    if subdataset in metrics
    }

    groups = {}
    groups['MMATH'] = GroupResult(
            metrics={
                'accuracy': MetricResult(
                    scores={
                        'accuracy': Score(
                            value=metrics['micro_avg'],
                            stats={},
                        )
                    }
                )
            }
        )    
    
    return EvaluationResult(tasks=tasks, groups=groups)
