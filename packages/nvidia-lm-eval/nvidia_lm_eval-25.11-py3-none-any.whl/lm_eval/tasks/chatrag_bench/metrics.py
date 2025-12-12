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

# The following code is adapted from
# https://github.com/facebookresearch/ParlAI/blob/master/parlai/core/metrics.py, 
# which is licensed under the MIT license. More details on the license can be 
# found at https://github.com/facebookresearch/ParlAI/blob/master/LICENSE.

"""Provides standard metric evaluations for dialog."""

from collections import Counter
from typing import List
import numpy as np
import re

re_art = re.compile(r'\b(a|an|the)\b')
re_punc = re.compile(r'[!"#$%&()*+,-./:;<=>?@\[\]\\^`{|}~_\']')


def normalize_answer(s):
    """
    Lower text and remove punctuation, articles and extra whitespace.
    """
    s = s.lower()
    s = re_punc.sub(' ', s)
    s = re_art.sub(' ', s)
    s = ' '.join(s.split())
    return s


class F1Metric:
    """
    Helper class which computes token-level F1.
    """

    @staticmethod
    def _prec_recall_f1_score(pred_items, gold_items):
        """
        Compute precision, recall and f1 given a set of gold and prediction items.
        :param pred_items: iterable of predicted values
        :param gold_items: iterable of gold values
        :return: tuple (p, r, f1) for precision, recall, f1
        """
        common = Counter(gold_items) & Counter(pred_items)
        num_same = sum(common.values())
        if num_same == 0:
            return 0, 0, 0
        precision = 1.0 * num_same / len(pred_items)
        recall = 1.0 * num_same / len(gold_items)
        f1 = (2 * precision * recall) / (precision + recall)
        return precision, recall, f1

    @staticmethod
    def compute_each_pair(guess: str, answer: str):
        if answer == "":
            return None, None, None
        if guess == "":
            return 0, 0, 0
        g_tokens = normalize_answer(guess).split()
        a_tokens = normalize_answer(answer).split()

        precision, recall, f1 = F1Metric._prec_recall_f1_score(g_tokens, a_tokens)
        return precision, recall, f1
        
    @staticmethod
    def compute_all_pairs(guesses: List[str], answers: List[list]):
        assert len(guesses) == len(answers)
        precision_list, recall_list, f1_list = [], [], []
        for guess, answer in zip(guesses, answers):
            assert type(answer) == str
            answer = answer.strip()
            precision, recall, f1 = F1Metric.compute_each_pair(guess, answer)
            
            precision_list.append(precision)
            recall_list.append(recall)
            f1_list.append(f1)
        
        return np.mean(precision_list), np.mean(recall_list), np.mean(f1_list)