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

from typing import List

import yaml


def generate_yaml_content(vocab_name: str, level: str):
    content = {
        "dataset_name": f"{vocab_name}_{level}",
        "tag": f"med_concepts_qa_{vocab_name}_tasks",
        "include": "_default_template_yaml",
        "task": f"med_concepts_qa_{vocab_name}_{level}",
        "task_alias": f"{vocab_name}_{level}",
    }
    return content


def generate_yaml_files(
    vocab_names: List[str], levels: List[str], file_name_prefix: str
):
    for vocab_name in vocab_names:
        for level in levels:
            yaml_content = generate_yaml_content(vocab_name, level)
            filename = f"{file_name_prefix}_{vocab_name}_{level}.yaml"
            with open(filename, "w") as yaml_file:
                yaml.dump(yaml_content, yaml_file, default_flow_style=False)
            print(f"Done to generated {filename}")


if __name__ == "__main__":
    generate_yaml_files(
        vocab_names=["icd9cm", "icd10cm", "icd9proc", "icd10proc", "atc"],
        levels=["easy", "medium", "hard"],
        file_name_prefix="med_concepts_qa",
    )
