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

def mean_3class_f1(predictions, references):  # This is a passthrough function
    string_label = ["entailment", "contradiction", "neutral"]
    predictions = (
        string_label.index(predictions[0]) if predictions[0] in string_label else 0
    )
    references = string_label.index(references[0])

    return (predictions, references)


def agg_mean_3class_f1(items):
    predictions, references = zip(*items)

    """Computes the unweighted average of the F1 per class."""
    metric_str = "fbeta_score"
    metric_fn_kwargs = {
        "beta": 1,
        "labels": range(3),
        "average": "macro",
    }

    def _fn(predictions, references):
        import sklearn.metrics

        metric_fn = getattr(sklearn.metrics, metric_str)
        metric_val = metric_fn(references, predictions, **metric_fn_kwargs)
        return metric_val

    return _fn(predictions, references)
