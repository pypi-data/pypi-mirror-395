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

from collections import Counter
from string import punctuation

import numpy as np


def normalize(text):
    exclude = set(punctuation)
    return "".join(ch for ch in text if ch not in exclude).lower().strip()


def f1(prediction, completion):
    gold_toks = completion.split()
    pred_toks = prediction.split()
    common = Counter(gold_toks) & Counter(pred_toks)
    num_same = sum(common.values())
    if len(gold_toks) == 0 or len(pred_toks) == 0:
        return int(gold_toks == pred_toks)
    if num_same == 0:
        return 0
    precision = 1.0 * num_same / len(pred_toks)
    recall = 1.0 * num_same / len(gold_toks)
    f1 = (2 * precision * recall) / (precision + recall)
    return f1


def process_results(doc, results):
    prediction = normalize(results[0])
    completions = [normalize(completion) for completion in doc["accepted_completions"]]
    exact_match = np.nanmax(
        [int(prediction == completion) for completion in completions]
    )
    fscore = np.nanmax(
        [f1(prediction=prediction, completion=completion) for completion in completions]
    )
    return {"em": exact_match, "fscore": fscore}


def filter_dataset_nb(dataset):
    return dataset.filter(lambda example: example["language"] == "nob")


def filter_dataset_nn(dataset):
    return dataset.filter(lambda example: example["language"] == "nno")
