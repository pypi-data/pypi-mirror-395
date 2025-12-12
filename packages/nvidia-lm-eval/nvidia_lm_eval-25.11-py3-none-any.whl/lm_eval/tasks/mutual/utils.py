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

import numpy as np


def process_docs(dataset):
    def _detokenize(text):
        text = text.replace(" '", "'")
        text = text.replace(" \n", "\n")
        text = text.replace("\n ", "\n")
        text = text.replace(" n't", "n't")
        text = text.replace("`` ", '"')
        text = text.replace("''", '"')
        # punctuation
        text = text.replace(" :", ":")
        text = text.replace(" ;", ";")
        text = text.replace(" !", "!")
        text = text.replace(" ?", "?")
        text = text.replace(" ,", ",")
        text = text.replace(" .", ".")
        return text

    def _process(doc):
        return {
            "article": _detokenize(doc["article"]),
            "options": [_detokenize(option) for option in doc["options"]],
        }

    return dataset.map(_process)


def process_results(doc, results):
    gold = ["A", "B", "C", "D"].index(doc["answers"])
    r4_1 = np.argmax(results) == gold  # r4_1 = accuracy
    ranks = sorted(results, reverse=True)
    r4_2 = (ranks.index(results[gold]) == 1) + r4_1
    mrr = 1.0 / (ranks.index(results[gold]) + 1)  # `+ 1` for index offset
    return {"r@1": r4_1, "r@2": r4_2, "mrr": mrr}
