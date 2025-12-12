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

# Original Copyright EleutherAI.
# For the original license and copyright information, see the LICENSE file in this repository.

"""Generate a config per subset."""
from datasets import get_dataset_config_names
import os

data_name = "edinburgh-dawg/mmlu-redux"

# List all configs for this dataset
configs = get_dataset_config_names(data_name)

# Generate YAML files in the current directory
for subset in configs:
    filename = f"mmlu_redux_{subset}.yaml"
    content = f"""
dataset_name: {subset}
include: _default_template_yaml
task: mmlu_redux_{subset}
task_alias: {subset}
    """.strip()

    with open(filename, "w") as file:
        file.write(content)

    print(f"Generated: {filename}")
