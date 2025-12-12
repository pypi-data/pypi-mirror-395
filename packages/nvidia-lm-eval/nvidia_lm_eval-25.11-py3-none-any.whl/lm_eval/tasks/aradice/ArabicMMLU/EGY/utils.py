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

level_ar = {
    "Primary": "للمرحلة الابتدائية",
    "Middle": "للمرحلة المتوسطة",
    "High": "للمرحلة الثانوية",
    "Univ": "للمرحلة الجامعية ",
    "Prof": "للمحترفين",
}

country_ar = {
    "UAE": "في الإمارات",
    "Egypt": "في مصر",
    "Lebanon": "في لبنان",
    "Jordan": "في الأردن",
    "Kuwait": "في الكويت",
    "KSA": "في السعودية",
    "Palestine": "في فلسطين",
    "Morocco": "في المغرب",
}

subject_ar = {
    "Islamic Studies": "في الدراسات إسلامية",
    "Driving Test": "في اختبار القيادة",
    "Natural Science": "في العلوم الطبيعية",
    "History": "في مادة التاريخ",
    "General Knowledge": "في المعرفة العامة",
    "Law": "في القانون",
    "Physics": "في الفيزياء",
    "Social Science": "في العلوم الاجتماعية",
    "Management": "في الإدارة",
    "Arabic Language": "في اللغة العربية",
    "Political Science": " في العلوم السياسية",
    "Philosophy": "في الفلسفة",
    "Accounting": "في المحاسبة",
    "Computer Science": "في علوم الحاسوب",
    "Geography": "في الجغرافيا",
    "Math": "في الرياضيات",
    "Biology": "في علم الأحياء",
    "Economics": "في الاقتصاد",
    "Arabic Language (General)": "في اللغة العربية (عام)",
    "Arabic Language (Grammar)": "في اللغة العربية (النحو)",
    "Civics": "في التربية المدنية",
}


alpa_ar = ["أ-", "ب-", "ج-", "د-", "و-"]
alpa_en = ["A-", "B-", "C-", "D-", "E-"]
all_choices = ["أ", "ب", "ج", "د", "و"]
all_choices_en = ["A", "B", "C", "D", "E"]


def process_docs(dataset):
    def _helper(doc):
        # modifies the contents of a single
        # document in our dataset.

        PROMPT = "ده سؤال [MAIN_META_DATA]. اختار الإجابة الصحيحة!\n\nسؤال: [INPUT]\n[OPTION]"
        PROMPT = f"{PROMPT}\n\nإجابة:"
        alpa = alpa_ar
        subject = subject_ar[doc["Subject"]]
        level = " " + level_ar[doc["Level"]] if doc["Level"] else ""
        country = " " + country_ar[doc["Country"]] if doc["Country"] else ""
        main_meta_data = f"{subject}{level}{country}"

        question = (
            f"{doc['context']}\n\n{doc['question']}"
            if doc["context"]
            else doc["question"]
        )
        options = []
        for i, opt in enumerate(["A", "B", "C", "D", "E"]):
            if opt not in doc["options"] or doc["options"][opt] is None:
                break
            options.append(f"{alpa[i]} {doc['options'][opt]}")

        doc["prompt"] = (
            PROMPT.replace("[MAIN_META_DATA]", main_meta_data)
            .replace("[INPUT]", question)
            .replace("[OPTION]", "\n".join(options))
        )

        doc["choices"] = all_choices[: len(options)]

        doc["target"] = ["A", "B", "C", "D", "E"].index(doc["Answer Key"])

        return doc

    return dataset.map(_helper)  # returns back a datasets.Dataset object
