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
    def _helper(doc):
        # Assuming that the 'answer' field in the dataset now contains numbers 0-3 instead of 'A', 'B', 'C', 'D'
        answer_list = ["A", "B", "C", "D"]
        # Convert numeric index to corresponding letter
        answer_index = int(doc["answer"])  # Make sure the answer is an integer
        answer_letter = answer_list[answer_index]

        out_doc = {
            "questions": doc["question"],
            "choices": [doc["choice1"], doc["choice2"], doc["choice3"], doc["choice4"]],
            "answer": answer_letter,  # Include the letter for clarity
        }
        return out_doc

    return dataset.map(_helper)
