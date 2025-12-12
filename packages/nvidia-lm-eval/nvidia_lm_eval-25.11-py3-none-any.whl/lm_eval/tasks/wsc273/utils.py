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

upper_pronouns = [
    "A",
    "An",
    "The",
    "She",
    "He",
    "It",
    "They",
    "My",
    "His",
    "Her",
    "Their",
]


def process_doc(dataset):
    def process_fn(doc):
        # The HF implementation of `wsc273` is not `partial evaluation` friendly.
        doc["text"] = doc["text"].replace("  ", " ")
        doc["options"][0] = __normalize_option(doc, doc["options"][0])
        doc["options"][1] = __normalize_option(doc, doc["options"][1])
        return doc

    return dataset.map(process_fn)


def __normalize_option(doc, option):
    # Append `'s` to possessive determiner based options.
    if doc["pronoun"].lower() in ["my", "his", "her", "our", "their"]:
        option += "'s"
    # Appropriately lowercase the pronoun in the option.
    pronoun = option.split()[0]
    start_of_sentence = doc["text"][doc["pronoun_loc"] - 2] == "."
    if not start_of_sentence and pronoun in upper_pronouns:
        return option.replace(pronoun, pronoun.lower())
    return option
