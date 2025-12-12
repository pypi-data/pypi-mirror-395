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

def process_docs(dataset: datasets.Dataset) -> datasets.Dataset:
    """Filters dataset and sets the correct answer."""
    filtered_data = []
    for item in dataset:
        if item["error_type"] == "ok":
            correct_answer = item["answer"]
        elif item["error_type"] == "wrong_groundtruth" and item["correct_answer"]:
            try:
                correct_answer = int(item["correct_answer"])
            except ValueError:
                correct_answer = list("ABCD").index(item["correct_answer"])
        else:
            # multiple answers, bad questions, etc.
            continue
        filtered_data.append({
            "question": item["question"],
            "choices": item["choices"],
            "correct_answer": correct_answer,
        })

    return datasets.Dataset.from_list(filtered_data)