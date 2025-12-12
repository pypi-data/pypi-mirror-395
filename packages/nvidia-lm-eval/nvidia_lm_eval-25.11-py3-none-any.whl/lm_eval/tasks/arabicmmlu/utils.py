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

PROMPT = "This is a {}. Select the correct answer!\n\nQuestion: {}\n{}\n\nAnswer:"

level_en = {
    "Primary": "primary school",
    "Middle": "middle school",
    "High": "high school",
    "Univ": "university",
    "Prof": "professional",
}

alpa = ["A.", "B.", "C.", "D.", "E."]


def doc_to_text(doc):
    """
    Refactoring `prepare_data_en` to fit with the lm harness framework.
    https://github.com/mbzuai-nlp/ArabicMMLU/blob/main/util_prompt.py
    """

    level = "" if not doc["Level"] else " for " + level_en[doc["Level"]]
    country = "" if not doc["Country"] else " in " + doc["Country"]
    main_meta_data = f"{doc['Subject']} question{level}{country}"

    question = (
        doc["Question"]
        if not doc["Context"]
        else f"{doc['Context']}\n\n{doc['Question']}"
    )

    options = []
    for i, opt in enumerate(
        ["Option 1", "Option 2", "Option 3", "Option 4", "Option 5"]
    ):
        if not doc[opt]:
            break
        options.append(f"{alpa[i]} {doc[opt]}")

    doc_text = PROMPT.format(main_meta_data, question, "\n".join(options))

    return doc_text


def doc_to_choice(doc):
    return [alpa[i][0] for i in range(5) if doc[f"Option {i + 1}"]]
