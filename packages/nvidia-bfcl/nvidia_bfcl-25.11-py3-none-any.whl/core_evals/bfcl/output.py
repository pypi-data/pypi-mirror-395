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
from pathlib import Path
import yaml
import pandas as pd
import functools
import operator
from nemo_evaluator.api.api_dataclasses import EvaluationResult

# results:
#   groups:
#     ifeval:
#       metrics:
#         inst_level_loose_acc:
#           scores:
#             inst_level_loose_acc:
#               stats:
#                 stderr: N/A
#               value: 0.7666666666666667


def bfcl_to_standard_output(partial_data: dict, suffix: str) -> dict:
    partial_data_standard_output = {}
    for metric, value in partial_data.items():
        if pd.isna(value):
            continue
        value = float(value.strip('%'))

        if not('overall' in metric.lower() or 'summary' in metric.lower()):
            metric += suffix
        partial_data_standard_output[metric] = value
    return partial_data_standard_output


# This is the only required function
def parse_output(output_dir: str) -> dict:
    result_dict = {}
    output_dir = Path(output_dir)
    with open(os.path.join(output_dir, 'run_config.yml'), "r") as f:
        yaml_config = yaml.safe_load(f)

    model_id = yaml_config['target']['api_endpoint']['model_id'].replace("/", "_")
    data_live = pd.read_csv(output_dir / 'score' /  'data_live.csv').set_index("Model").loc[model_id].drop("Rank").to_dict()
    data_nonlive = pd.read_csv(output_dir / 'score' / 'data_non_live.csv').set_index("Model").loc[model_id].drop("Rank").to_dict()
    data_multiturn = pd.read_csv(output_dir / 'score' / 'data_multi_turn.csv').set_index("Model").loc[model_id].drop("Rank").to_dict()
    stdout_live = bfcl_to_standard_output(data_live, ' Live')
    stdout_nonlive = bfcl_to_standard_output(data_nonlive, ' Non-Live')
    stdout_multiturn = bfcl_to_standard_output(data_multiturn, '')
    stdout = functools.reduce(operator.or_, [stdout_live, stdout_nonlive, stdout_multiturn])
    for metric, value in stdout.items():
        metric = metric.lower().replace(" ", "_").replace("-", "_")
        result_dict[metric] = {"scores": {metric: {'value' : value, "stats": {}}}}
    return EvaluationResult(groups={"bfcl": {"metrics": result_dict}})
