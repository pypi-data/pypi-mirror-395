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

import datasets


def process_docs(dataset: datasets.Dataset) -> datasets.Dataset:
    def _process_doc(doc):
        instruction = f"""다음을 읽고 정답으로 알맞은 것을 고르시요.
### Context: {doc["context"]}
### Question: {doc["question"]}
### Options:
(1) {doc["option#1"]}\n(2) {doc["option#2"]}\n(3) {doc["option#3"]}\n(4) {doc["option#4"]}\n(5) {doc["option#5"]}
### Answer: 주어진 문제의 정답은"""

        out_doc = {
            "question": instruction,
            "choices": ["(1)", "(2)", "(3)", "(4)", "(5)"],
            "gold": int(doc["gold"]) - 1,
        }
        return out_doc

    return dataset.map(_process_doc)
