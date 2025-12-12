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
import numpy as np


def process_docs(dataset: datasets.Dataset):
    def _process_doc(doc):
        premise = doc["premise"]
        choices = [doc["choice1"], doc["choice2"]]
        question_map = {"cause": "لأن", "effect": "لذلك"}
        question = question_map[doc["question"]]
        answer = doc["label"]

        query = "{}، {} :\n0) {}\n1) {}\nالإجابة:".format(
            premise, question, choices[0], choices[1]
        )

        return {"query": query, "choices": choices, "gold": answer}

    return dataset.map(_process_doc)
