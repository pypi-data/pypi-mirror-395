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

import math
import re


def calculate_score_fullscale(docs, results):
    reference = eval(docs["reference_answer_fullscale"])
    user = dict(re.findall(r"(\w+):\s+(\d+)", results[0]))
    # First check that the emotions specified in the answer match those in the reference
    if len(user.items()) != 4:
        # print('! Error: 4 emotions were not returned')
        # print(user)
        return {"eqbench": 0, "percent_parseable": 0}
    emotions_dict = {}
    for emotion, user_emotion_score in user.items():
        for i in range(1, 5):
            if emotion == reference[f"emotion{i}"]:
                emotions_dict[emotion] = True
    if len(emotions_dict) != 4:
        print("! Error: emotions did not match reference")
        print(user)
        return {"eqbench": 0, "percent_parseable": 0}

    difference_tally = (
        0  # Tally of differerence from reference answers for this question
    )

    # Iterate over each emotion in the user's answers.
    for emotion, user_emotion_score in user.items():
        # If this emotion is in the reference, calculate the difference between the user's score and the reference score.
        for i in range(1, 5):
            if emotion == reference[f"emotion{i}"]:
                d = abs(
                    float(user_emotion_score) - float(reference[f"emotion{i}_score"])
                )
                # this will be a value between 0 and 10
                if d == 0:
                    scaled_difference = 0
                elif d <= 5:
                    # S-shaped scaling function
                    # https://www.desmos.com/calculator
                    # 6.5\cdot\ \frac{1}{\left(1\ +\ e^{\left(-1.2\cdot\left(x-4\right)\right)}\right)}
                    scaled_difference = 6.5 * (1 / (1 + math.e ** (-1.2 * (d - 4))))

                else:
                    scaled_difference = d
                difference_tally += scaled_difference

    # Inverting the difference tally so that the closer the answer is to reference, the higher the score.
    # The adjustment constant is chosen such that answering randomly produces a score of zero.
    adjust_const = 0.7477
    final_score = 10 - (difference_tally * adjust_const)
    final_score_percent = final_score * 10

    return {"eqbench": final_score_percent, "percent_parseable": 100}
