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

from lm_eval.api.filter import Filter
from lm_eval.api.registry import register_filter


alpha = ["A", "B", "C"]
out_dic = {"ايجابي": 1, "سلبي": 0, "ماكينش إحساس": 2}


def doc_to_text(doc):
    return (
        doc["messages"][0]["content"]
        .replace("-سلبي", "A. سلبي")
        .replace("-ايجابي", "B. ايجابي")
        .replace(
            "-ماكينش إحساس",
            "C. ماكينش إحساس\nThe answer should be strictly one letter of the following: A, B, C.",
        )
    )  # .replace('شنو هو الإحساس ديال هاد الجملة؟', 'شنو هو الإحساس ديال هاد الجملة؟')


def doc_to_choice_3(doc):
    return alpha


def doc_to_choice_2(doc):
    return alpha[:2]


def doc_to_target(doc):
    return alpha[out_dic[doc["messages"][1]["content"]]]
