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

from functools import partial


def convert_choice(choice):
    return choice[0].lower() + choice[1:]


def doc_to_text(doc, connector):
    # Drop the period
    conn = connector[doc["question"]]
    return doc["premise"].strip()[:-1] + f" {conn}"


def doc_to_choice(doc):
    return [convert_choice(doc["choice1"]), convert_choice(doc["choice2"])]


doc_to_text_et = partial(
    doc_to_text,
    connector={
        "cause": "sest",
        "effect": "seetõttu",
    },
)


doc_to_text_ht = partial(
    doc_to_text,
    connector={
        "cause": "poukisa",
        "effect": "donk sa",
    },
)


doc_to_text_it = partial(
    doc_to_text,
    connector={
        "cause": "perché",
        "effect": "quindi",
    },
)


doc_to_text_id = partial(
    doc_to_text,
    connector={
        "cause": "karena",
        "effect": "maka",
    },
)


doc_to_text_qu = partial(
    doc_to_text,
    connector={
        "cause": "imataq",
        "effect": "chaymi",
    },
)


doc_to_text_sw = partial(
    doc_to_text,
    connector={
        "cause": "kwa sababu",
        "effect": "kwa hiyo",
    },
)


doc_to_text_zh = partial(
    doc_to_text,
    connector={
        "cause": "因为",
        "effect": "所以",
    },
)


doc_to_text_ta = partial(
    doc_to_text,
    connector={
        "cause": "காரணமாக",
        "effect": "எனவே",
    },
)


doc_to_text_th = partial(
    doc_to_text,
    connector={
        "cause": "เพราะ",
        "effect": "ดังนั้น",
    },
)


doc_to_text_tr = partial(
    doc_to_text,
    connector={
        "cause": "çünkü",
        "effect": "bu yüzden",
    },
)


doc_to_text_vi = partial(
    doc_to_text,
    connector={
        "cause": "bởi vì",
        "effect": "vì vậy",
    },
)
