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

LANG_NAMES = {
    'cs': 'Czech',
    'uk': 'Ukrainian',
    'de': 'German',
    'en': 'English',
    'he': 'Hebrew',
    'ja': 'Japanese',
    'ru': 'Russian',
    'zh': 'Chinese'
}

ALL_TRANSLATIONS = [
'cs-uk',
'de-en',
'en-cs',
'en-de',
'en-he',
'en-ja',
'en-ru',
'en-uk',
'en-zh',
'he-en',
'ja-en',
'ru-en',
'uk-en',
'zh-en',
]



if __name__ == "__main__":
    for lang_pair in ALL_TRANSLATIONS:
        target_language = LANG_NAMES[lang_pair.split('-')[1]]
        yaml_dict = {
            "include": "wmt23_yaml",
            "task": f"wmt23_{lang_pair}",
            "dataset_kwargs": {
                "data_files": {
                    "train": f"/datasets/wmt23/samples_{lang_pair}.json",
                    "test": f"/datasets/wmt23/test_{lang_pair}.json",
                },
            },
            "doc_to_text": f"What is the " + target_language + r" translation of the sentence: {{src}}?\n"
        }

        file_save_path = f"wmt23_{lang_pair}.yaml"
        with open(file_save_path, "w", encoding="utf-8") as yaml_file:
            yaml.dump(
                yaml_dict,
                yaml_file,
                width=float("inf"),
                allow_unicode=True,
            )