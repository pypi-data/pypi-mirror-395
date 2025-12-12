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

choices = [
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "I",
    "J",
    "K",
    "L",
    "M",
    "N",
    "O",
    "P",
]


def format_cot_example(example, including_answer=True):
    prompt = "Question:\n"
    question = example["question"]
    options = example["options"]
    prompt += question + "\n"
    prompt += "Options:\n"
    for i, opt in enumerate(options):
        prompt += "{}. {}\n".format(choices[i], opt)
    if including_answer:
        cot_content = example["cot_content"].replace(
            "A: Let's think step by step.", "Answer: Let's think step by step."
        )
        prompt += cot_content + "\n\n"
    else:
        prompt += "Answer: Let's think step by step."
    return prompt


def fewshot_to_target_for_chat_multiturn(example: dict) -> str:
    """Returns a target (answer) for fewshot multiturn enabled.

    NOTE(agronskiy): added as a fix to the following bug: when --fewshot_as_multiturn is
    enabled (which is the case for chat template), default MMLU-Pro behavior would be to add the answer to the
    'user' messages, leaving `assistant` empty inbetween. To fix that, we introduce this
    function that adds CoT content to the `assistant`. Additionally, it removes the `Let's
    think step by step` because MMLU-Pro formats this as the end of user's message (see L37
    above, so we should not duplicate).

    Examples of the above:

    Before:
        - user: "some question. Answer: let's think step by step. Here's some reasoning. The answer is (D)"
        - assistant: ""
        - user: "some question. Answer: let's think step by step. Here's some reasoning. The answer is (D)"
        - assistant: ""
        - user: "final question. Answer: let's think step by step."
    After:
        - user: "some question. Answer: let's think step by step."
        - assistant: "here's some reasoning. The answer is (D)"
        - user: "some question. Answer: let's think step by step."
        - assistant: "here's some reasoning. The answer is (D)"
        - user: "final question. Answer: let's think step by step"

    """
    prompt = ""
    cot_content = example["cot_content"].replace("A: Let's think step by step.", "")
    # Usually, there's a whitespace in the answer after "Let's think step by step"
    cot_content = cot_content.lstrip()
    prompt += cot_content + "\n\n"

    return prompt


doc_to_text = partial(format_cot_example, including_answer=False)
fewshot_to_text = partial(format_cot_example, including_answer=True)


def process_docs(dataset, subject):
    return dataset.filter(lambda x: x["category"] == subject)


process_biology = partial(process_docs, subject="biology")
process_business = partial(process_docs, subject="business")
process_chemistry = partial(process_docs, subject="chemistry")
process_computer_science = partial(process_docs, subject="computer science")
process_economics = partial(process_docs, subject="economics")
process_engineering = partial(process_docs, subject="engineering")
process_health = partial(process_docs, subject="health")
process_history = partial(process_docs, subject="history")
process_law = partial(process_docs, subject="law")
process_math = partial(process_docs, subject="math")
process_other = partial(process_docs, subject="other")
process_philosophy = partial(process_docs, subject="philosophy")
process_physics = partial(process_docs, subject="physics")
process_psychology = partial(process_docs, subject="psychology")
