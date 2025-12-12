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

import collections

import numpy as np


def f1(predictions, references):  # This is a passthrough function
    _prediction = predictions[0]
    _reference = references[0].split("_")[-1]
    string_label = ["False", "True"]
    reference = string_label.index(_reference)
    prediction = (
        string_label.index(_prediction)
        if _prediction in string_label
        else not bool(reference)
    )

    return (prediction, reference)


def agg_f1(items):
    from sklearn.metrics import f1_score

    predictions, references = zip(*items)
    references, predictions = np.asarray(references), np.asarray(predictions)

    return f1_score(references, predictions)


def em(predictions, references):  # This is a passthrough function
    _prediction = predictions[0]
    _group, _reference = references[0].split("_")
    string_label = ["False", "True"]
    reference = string_label.index(_reference)
    prediction = (
        string_label.index(_prediction)
        if _prediction in string_label
        else not bool(reference)
    )

    return (_group, prediction, reference)


def agg_em(items):
    grouped_values = collections.defaultdict(lambda: ([], []))
    for group, prediction, reference in items:
        grouped_values[group][0].append(reference)
        grouped_values[group][1].append(prediction)

    group_scores = []
    for group, (targets, predictions) in grouped_values.items():
        score = float(np.array_equal(targets, predictions))
        group_scores.append(score)

    return np.mean(group_scores)
