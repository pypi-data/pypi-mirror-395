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
import evaluate


def strip(resps, docs):
    """
    Assuming each entry of `resps` is a list of model responses, we discard all but the first response.
    """
    return map(lambda r: r[0].strip(), resps)


def doc_to_text(doc):
    doc_text = doc["messages"][0]["content"].replace(
        "لخص هاد المقطع", "لخص هاد المقطع في ٣٠ كلمة"
    )
    return doc_text


def doc_to_target(doc):
    return doc["messages"][1]["content"]


def bert(items):
    return items


def Average(lst):
    return sum(lst) / len(lst)


def darijabert(items):
    bert_model = "SI2M-Lab/DarijaBERT"
    bert_score = evaluate.load("bertscore")
    predictions, references = zip(*items)
    bert = bert_score.compute(
        predictions=predictions,
        references=references,
        model_type=bert_model,
        num_layers=12,
    )
    return Average(bert["f1"])


def rouge1(items):
    return items


def rougeL(items):
    return items


def rouge2(items):
    return items


def rougeLsum(items):
    return items


def agg_rougelsum(items):
    rouge = evaluate.load("rouge")
    predictions, references = zip(*items)
    return rouge.compute(predictions=predictions, references=references)["rougeLsum"]


def agg_rouge1(items):
    rouge = evaluate.load("rouge")
    predictions, references = zip(*items)
    return rouge.compute(predictions=predictions, references=references)["rouge1"]


def agg_rouge2(items):
    rouge = evaluate.load("rouge")
    predictions, references = zip(*items)
    return rouge.compute(predictions=predictions, references=references)["rouge2"]


def agg_rougel(items):
    rouge = evaluate.load("rouge")
    predictions, references = zip(*items)
    return rouge.compute(predictions=predictions, references=references)["rougeL"]
