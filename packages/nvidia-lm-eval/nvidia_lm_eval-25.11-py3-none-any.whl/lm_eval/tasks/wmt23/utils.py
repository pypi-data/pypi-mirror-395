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

import regex
import string

from rouge_score import rouge_scorer

def _normalize_answer(text):
    # NOTE(dfridman): copy-pase from lm_eval/tasks/nqopen.py
    # Lowercase and remove punctuation, strip whitespace
    text = text.strip().lower().translate(str.maketrans("", "", string.punctuation))

    # Remove articles, resulting in duplicate whitespace
    text = regex.sub(r"\b(a|an|the)\b", " ", text)

    # Remove duplicate whitespace
    text = " ".join(text.split())

    return text

def process_results(doc, results):
    rouge = rouge_scorer.RougeScorer(["rouge1", "rouge2", "rougeL"])

    gt = _normalize_answer(doc["trg"])
    pred = _normalize_answer(results[0])

    scores = rouge.score(gt, pred)
    scores = {
        metric_name: v.fmeasure for metric_name, v in scores.items()
    }
    return scores
