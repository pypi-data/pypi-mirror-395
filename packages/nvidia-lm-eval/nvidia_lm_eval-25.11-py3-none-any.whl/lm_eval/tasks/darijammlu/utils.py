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

PROMPT = "هادا سؤال متعدد الخيارات (مع الجواب ديالو) على {}\n\n{}\n{}\nالجواب:"


alpha = ["A.", "B.", "C.", "D.", "E."]


def doc_to_text(doc):
    subject = doc["subject_darija"]
    question = (
        doc["question"]
        if doc["context"] == ""
        else f"{doc['context']}\n\n{doc['question']}"
    )

    options = []
    for i, opt in enumerate(doc["choices"]):
        options.append(f"{alpha[i]} {opt}")

    doc_text = PROMPT.format(subject, question, "\n".join(options))

    return doc_text


def doc_to_choice(doc):
    return [alpha[i][0] for i in range(len(doc["choices"]))]
