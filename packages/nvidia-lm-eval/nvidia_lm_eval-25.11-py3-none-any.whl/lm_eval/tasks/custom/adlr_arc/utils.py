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

def doc_to_text_llama( doc):
    # NOTE: Some `doc["answerKey"]`s are in numeric string format being one
    # of {'1', '2', '3', '4', '5'}. We map them back to letters.
    letters = ["A", "B", "C", "D", "E"]
    query = f"""Question: {doc["question"]}"""
    for idx, c in enumerate(doc["choices"]["text"]):
        query += f"""\n{letters[idx]}. {doc["choices"]["text"][idx]}"""
    query += "\nAnswer:"

    return query

def doc_to_choice_llama(doc):
    letters = ["A", "B", "C", "D", "E"]
    choices = []
    for idx, _ in enumerate(doc["choices"]["text"]):
        choices.append(f"""{letters[idx]}""")
    return choices

def doc_to_target_llama(doc):
    # NOTE: Some `doc["answerKey"]`s are in numeric string format being one
    # of {'1', '2', '3', '4', '5'}. We map them back to letters.
    num_to_letter = {"1": "A", "2": "B", "3": "C", "4": "D", "5": "E"}
    doc["answerKey"] = num_to_letter.get(doc["answerKey"], doc["answerKey"])
    return ["A", "B", "C", "D", "E"].index(doc["answerKey"])