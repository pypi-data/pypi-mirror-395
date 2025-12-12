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

def p0_nn(doc):
    prompt = "Spørsmål: {question}\n\nSvar:"
    return prompt.format(question=doc["question"])


def p1_nn(doc):
    prompt = "Spørsmål: {question}\n\nSvaralternativ:{choices}\n\nSvar:"
    choices = "".join(
        list(map(lambda choice: f"\n- {choice}", doc["mc1_targets"]["choices"]))
    )
    return prompt.format(question=doc["question"], choices=choices)


def p2_nn(doc):
    prompt = "Spørsmål: {question}\n\nKva av følgande alternativ er rett svar på spørsmålet?{choices}"
    choices = "".join(
        list(map(lambda choice: f"\n- {choice}", doc["mc1_targets"]["choices"]))
    )
    return prompt.format(question=doc["question"], choices=choices)


def p3_nn(doc):
    prompt = "Gitt følgande spørsmål, kva av dei moglege svara under er rett?\nSpørsmål: {question}\n{choices}"
    choices = "".join(
        list(map(lambda choice: f"\n- {choice}", doc["mc1_targets"]["choices"]))
    )
    return prompt.format(question=doc["question"], choices=choices)


def p4_nn(doc):
    prompt = "{question}\nVel eit av følgande moglege svar:{choices}\n\nSvar:"
    choices = "".join(
        list(map(lambda choice: f"\n- {choice}", doc["mc1_targets"]["choices"]))
    )
    return prompt.format(question=doc["question"], choices=choices)
