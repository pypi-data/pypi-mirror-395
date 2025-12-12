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

import random

import datasets


def process_docs_hard(dataset: datasets.Dataset):
    return dataset


def process_docs(dataset: datasets.Dataset):
    def _helper(doc):
        return doc

    num_entries = len(dataset)
    ten_percent_index = int(0.1 * num_entries)

    # Select the first 10% of the dataset
    filtered_dataset = dataset.select(range(ten_percent_index))

    return filtered_dataset.map(_helper)


def doc_to_choice_easy(doc):
    return [
        "neoplasms",
        "digestive system diseases",
        "nervous system diseases",
        "cardiovascular diseases",
        "general pathological conditions",
    ]


def doc_to_text_easy(doc) -> str:
    choices = doc_to_choice_easy(doc)
    prompt = (
        "Classify the topic of the following medical text into one of the following choices. \n"
        "Text: {} \n"
        "Choices: \n"
        "A. {} \n"
        "B. {} \n"
        "C. {} \n"
        "D. {} \n"
        "E. {} \n Answer:".format(
            doc["text"], choices[0], choices[1], choices[2], choices[3], choices[4]
        )
    )

    return prompt


def doc_to_target_easy(doc):
    return int(doc["class"]) - 1


def doc_to_text_hard(doc) -> str:
    choices = doc_to_choice_hard(doc)
    prompt = (
        "Select the medical specialty the following text is talking about among the following choices. \n"
        "Text: {} \n"
        "Choices: {}\n"
        " Answer:".format(doc["transcription"], choices)
    )

    return prompt


def doc_to_choice_hard(doc):
    choices_list = [
        " Bariatrics",
        " Allergy / Immunology",
        " Dentistry",
        " Cardiovascular / Pulmonary",
        " Urology",
        " Hospice - Palliative Care",
        " Radiology",
        " Pediatrics - Neonatal",
        " Neurology",
        " Neurosurgery",
        " Emergency Room Reports",
        " IME-QME-Work Comp etc.",
        " Office Notes",
        " Surgery",
        " Letters",
        " Ophthalmology",
        " Hematology - Oncology",
        " Endocrinology",
        " Cosmetic / Plastic Surgery",
        " Diets and Nutritions",
        " Rheumatology",
        " Nephrology",
        " Physical Medicine - Rehab",
        " Podiatry",
        " Chiropractic",
        " Lab Medicine - Pathology",
        " Orthopedic",
        " Autopsy",
        " Psychiatry / Psychology",
        " Speech - Language",
        " ENT - Otolaryngology",
        " Sleep Medicine",
        " Dermatology",
        " SOAP / Chart / Progress Notes",
        " General Medicine",
        " Consult - History and Phy.",
        " Obstetrics / Gynecology",
        " Gastroenterology",
        " Pain Management",
        " Discharge Summary",
    ]
    return choices_list


def doc_to_target_hard(doc):
    choices = doc_to_choice_hard(doc)
    gold = doc["medical_specialty"]
    idx = choices.index(gold)
    return idx
