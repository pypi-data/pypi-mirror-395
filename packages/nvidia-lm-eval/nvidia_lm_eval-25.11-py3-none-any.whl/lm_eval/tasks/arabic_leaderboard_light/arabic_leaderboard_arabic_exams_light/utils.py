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


# fmt: off
LETTER_INDICES_AR = ["أ", "ب", "ج", "د", "هـ", "و", "ز", "ح", "ط", "ي", "ك", "ل", "م", "ن", "س", "ع", "ف", "ص", "ق", "ر", "ش", "ت", "ث", "خ", "ذ", "ض", "ظ", "غ"]
# fmt: on


# fmt: off
LETTER_INDICES = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
# fmt: on


def process_docs(dataset: datasets.Dataset):
    def _process_doc(doc):
        topic = doc["subject"]
        question = doc["question"]
        choices = [doc["A"], doc["B"], doc["C"], doc["D"]]
        choices_formatted = [
            f" {LETTER_INDICES_AR[i]}) {choice}\n" for i, choice in enumerate(choices)
        ]
        answer = doc["answer"]
        answer_index = LETTER_INDICES.index(answer)

        instruction = f"الأسئلة التالية هي أسئلة متعددة الإختيارات مع الجواب الصحيح حول {topic.replace('_', ' ')}. \n\n"
        query = f"{instruction}السؤال: {question}\n"
        query += "\n".join(choices_formatted)
        query += "\nالإجابة:"

        return {"query": query, "choices": LETTER_INDICES_AR[:4], "gold": answer_index}

    return dataset.map(_process_doc)
