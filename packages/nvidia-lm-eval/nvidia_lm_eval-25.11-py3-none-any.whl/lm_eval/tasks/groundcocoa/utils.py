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
import pandas as pd
from datasets import Dataset


def process_docs(dataset: datasets.Dataset) -> datasets.Dataset:
    cocoa_dataset = [sample for sample in dataset]
    processed = []
    for doc in cocoa_dataset:
        question = "A user has specified certain criteria for booking a flight. Below are five different flight options labeled 'A', 'B', 'C', 'D', and 'E'. Review these options and select the one that best matches the user requirements. Respond with a single option and the phrase 'The answer is Option ' followed by the correct letter - 'A', 'B', 'C', 'D', or 'E'\n\n"
        question = question + "User Criteria: " + doc["query"]
        question = question + "\n\n Option A: " + str(doc["Option A"]) + "\n"
        question = question + "\n Option B: " + str(doc["Option B"]) + "\n"
        question = question + "\n Option C: " + str(doc["Option C"]) + "\n"
        question = question + "\n Option D: " + str(doc["Option D"]) + "\n"
        question = question + "\n Option E: " + str(doc["Option E"]) + "\n"
        out_doc = {
            "criteria": question,
            "choices": [
                "The answer is Option A",
                "The answer is Option B",
                "The answer is Option C",
                "The answer is Option D",
                "The answer is Option E",
            ],
            "gold": "The answer is Option " + doc["Answer"],
        }
        processed.append(out_doc)
    df = pd.DataFrame(processed)
    dataset = Dataset.from_pandas(df)
    return dataset
