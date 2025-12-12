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

from math_verify import parse, verify


def safe_parse(s: str) -> list[str]:
    try:
        return parse(s)
    except Exception as e:
        print(e, s)
        return ["[invalid]"]


def doc_to_target(doc: dict) -> str:
    if "answer" in doc:
        return doc["answer"].split("####")[-1].strip()
    else:
        assert "target" in doc
        return doc["target"]


def process_results(doc: dict, results: list[list[str]]) -> dict[str, int]:
    pred_answer = results[0]
    while isinstance(pred_answer, list):
        pred_answer = pred_answer[0]
    assert isinstance(pred_answer, str)

    gt_answer = safe_parse(doc_to_target(doc))
    pred_answer = safe_parse(pred_answer)
    exact_match = verify(gt_answer, pred_answer)
    parsed_pred_answer_str = pred_answer[-1] if pred_answer else "[invalid]"

    return {
        "exact_match": int(exact_match),
        "parse_meta": {
            "math_verify": {
                "gold": gt_answer[-1],
                "parsed": parsed_pred_answer_str,
                "exact_match": int(exact_match),
            }
        },
    }
