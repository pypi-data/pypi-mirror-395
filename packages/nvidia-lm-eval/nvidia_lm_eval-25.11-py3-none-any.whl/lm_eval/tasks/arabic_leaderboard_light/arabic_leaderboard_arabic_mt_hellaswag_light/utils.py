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

import re

import datasets
import numpy as np


def process_docs(dataset: datasets.Dataset):
    def _process_doc(doc):
        ctx = re.sub(r"\[.*?\]", "", doc["ctx"])  # Remove latin words within brackets
        endings = [
            re.sub(r"\[.*?\]", "", e) for e in eval(doc["endings"])
        ]  # endings is a string representation of a list
        answer_index = doc["label"]
        instruction = (
            "بناء على السياق التالي، اختر النهاية الصحيحة من الاقتراحات التالية"
        )

        query = f"""{instruction}
        السياق:
        {ctx}
        الاقتراحات:

        """
        for i, ending in enumerate(endings):
            query += f"{i}) {ending}\n"
        query += "الإجابة:"

        return {"query": query, "choices": endings, "gold": answer_index}

    return dataset.map(_process_doc)
