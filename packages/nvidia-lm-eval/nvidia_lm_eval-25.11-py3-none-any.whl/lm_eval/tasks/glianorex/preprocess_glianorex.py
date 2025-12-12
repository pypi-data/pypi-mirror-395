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

import datasets


def doc_to_text(doc) -> str:
    option_choices = doc["options"]
    answers = "".join((f"{k}. {v}\n") for k, v in option_choices.items())
    return f"Question: {doc['question']}\n{answers}Answer:"


def doc_to_target(doc) -> str:
    # answer_idx is `A`, `B`, `C`, `D` etc.
    return doc["answer_idx"]


def filter_dataset(dataset: datasets.Dataset, lang: str) -> datasets.Dataset:
    return dataset.filter(lambda example: example["language"].startswith(lang))


def filter_french(dataset: datasets.Dataset) -> datasets.Dataset:
    return filter_dataset(dataset, "fr")


def filter_english(dataset: datasets.Dataset) -> datasets.Dataset:
    return filter_dataset(dataset, "en")
