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

import random

import datasets
import numpy as np


def doc_to_text(doc):
    instruction = (
        "بناءً على السياق أدناه، اختر الإجابة الصحيحة للسؤال التالي من قائمة الاقتراحات"
    )
    support = doc["support"]
    question = doc["question"]
    query = f"""{instruction}
    السياق:
    {support}
    السؤال:
    {question}
    الإجابات المحتملة:

    """
    return query


def process_docs(dataset: datasets.Dataset):
    def _process_doc(doc):
        correct_answer = doc["correct_answer"]
        choices = [
            doc["distractor1"],
            doc["distractor2"],
            doc["distractor3"],
            correct_answer,
        ]

        # Shuffle the choices
        random.shuffle(choices)

        answer_index = choices.index(correct_answer)

        return {"query": doc_to_text(doc), "choices": choices, "gold": answer_index}

    return dataset.map(_process_doc)
