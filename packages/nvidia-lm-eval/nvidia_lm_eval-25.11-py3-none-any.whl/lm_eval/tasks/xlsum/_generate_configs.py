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

import yaml

ALL_LANGS = ['amharic',
    'arabic',
    'azerbaijani',
    'bengali',
    'burmese',
    'chinese_simplified',
    'chinese_traditional',
    'english',
    'french',
    'gujarati',
    'hausa',
    'hindi',
    'igbo',
    'indonesian',
    'japanese',
    'kirundi',
    'korean',
    'kyrgyz',
    'marathi',
    'nepali',
    'oromo',
    'pashto',
    'persian',
    'pidgin',
    'portuguese',
    'punjabi',
    'russian',
    'scottish_gaelic',
    'serbian_cyrillic',
    'serbian_latin',
    'sinhala',
    'somali',
    'spanish',
    'swahili',
    'tamil',
    'telugu',
    'thai',
    'tigrinya',
    'turkish',
    'ukrainian',
    'urdu',
    'uzbek',
    'vietnamese',
    'welsh',
    'yoruba',
]


if __name__ == "__main__":
    for lang_name in ALL_LANGS:
        yaml_dict = {
            "include": "xlsum_yaml",
            "task": f"xlsum_{lang_name}",
            "dataset_name": lang_name,
        }

        file_save_path = f"xlsum_{lang_name}.yaml"
        with open(file_save_path, "w", encoding="utf-8") as yaml_file:
            yaml.dump(
                yaml_dict,
                yaml_file,
                width=float("inf"),
                allow_unicode=True,
            )