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


_INVALID_ANSWER = "[invalid]"

_ANSWER_REGEX = re.compile(r"(\-?[0-9\.\,]+)")


def _extract_answer(completion):
    matches = _ANSWER_REGEX.findall(completion)
    if matches:
        match_str = matches[-1].strip(".")
        match_str = match_str.replace(",", "")
        try:
            match_float = float(match_str)
        except ValueError:
            return _INVALID_ANSWER

        if match_float.is_integer():
            return int(match_float)

    return _INVALID_ANSWER


def process_results(doc, results):
    assert len(results) == 1, (
        f"results should be a list with 1 str element, but is {results}"
    )

    completion = results[0]
    extracted_answer = _extract_answer(completion)
    answer = doc["answer_number"]
    acc = extracted_answer == answer
    return {
        "acc": acc,
    }
