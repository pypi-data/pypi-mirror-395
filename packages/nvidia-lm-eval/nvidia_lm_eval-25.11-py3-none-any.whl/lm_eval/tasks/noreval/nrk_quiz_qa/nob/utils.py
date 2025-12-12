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

def p0_nb(doc):
    prompt = "Spørsmål: {question}\n\nSvar:"
    return prompt.format(question=doc["question"])


def p1_nb(doc):
    prompt = "{question}\n\nSvaralternativer:{choices}\n\nHva er riktig svar?\n\nSvar:"
    choices = "".join(list(map(lambda choice: f"\n- {choice}", doc["choices"]["text"])))
    return prompt.format(question=doc["question"], choices=choices)


def p2_nb(doc):
    prompt = (
        "{question}{choices}\n\nEr det riktige svaret {enumerated_choices}?\n\nSvar:"
    )
    choices = "".join(
        [
            f"\n{label}: {option}"
            for label, option in zip(doc["choices"]["label"], doc["choices"]["text"])
        ]
    )
    enumerated_choices = ", ".join(
        doc["choices"]["label"][:-1]
    ) + ", eller {latest_choice}".format(latest_choice=doc["choices"]["label"][-1])
    if len(doc["choices"]["label"]) == 2:
        enumerated_choices = enumerated_choices.replace(", eller", " eller")
    return prompt.format(
        question=doc["question"], choices=choices, enumerated_choices=enumerated_choices
    )


def p3_nb(doc):
    prompt = "Spørsmål: {question}{choices}\n\nSvar:"
    choices = "".join(
        [
            f"\n{label}: {option}"
            for label, option in zip(doc["choices"]["label"], doc["choices"]["text"])
        ]
    )
    return prompt.format(question=doc["question"], choices=choices)


def p4_nb(doc):
    prompt = "{question}\nVelg riktig svar blant disse alternativene:{choices}\n\nSvar:"
    choices = "".join(list(map(lambda choice: f"\n- {choice}", doc["choices"]["text"])))
    return prompt.format(question=doc["question"], choices=choices)
