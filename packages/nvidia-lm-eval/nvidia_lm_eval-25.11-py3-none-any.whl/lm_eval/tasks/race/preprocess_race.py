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

import ast


def process_ast(string):
    return ast.literal_eval(string)


def last_problem(doc):
    return process_ast(doc["problems"])[-1]


def get_answer_option(problem):
    letter_to_num = {"A": 0, "B": 1, "C": 2, "D": 3}
    answer = letter_to_num[problem["answer"]]
    return problem["options"][answer]


def doc_to_choice(doc):
    problem = last_problem(doc)
    choices = [problem["options"][i] for i in range(4)]
    return choices


def doc_to_text(doc):
    text = "Article: " + doc["article"] + "\n\n"
    for problem in process_ast(doc["problems"])[:-1]:
        if problem["question"][-6:] == "  _  .":
            text += problem["question"][-5:] + get_answer_option(problem) + "\n"
        else:
            question = "Question: " + problem["question"] + "\n"
            answer = "Answer: " + get_answer_option(problem) + "\n"
            text += question + answer
    text += last_problem(doc)["question"]
    return text


def doc_to_target(doc):
    letter_to_num = {"A": 0, "B": 1, "C": 2, "D": 3}
    answer = letter_to_num[last_problem(doc)["answer"]]
    return answer
