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


CATEGORIES = [
    "Applied Science",
    "Arts & Humanities",
    "Business & Commerce",
    "Driving License",
    "General knowledge",
    "Health oriented education",
    "Marine License",
    "Medical License",
    "Professional certification",
    "STEM",
    "Social Science",
]


def process_docs(dataset, category):
    return dataset.filter(lambda x: x["domain"] == category)


process_functions = {
    f"process_{category.lower().replace(' & ', '_').replace(' ', '_')}": partial(
        process_docs, category=category
    )
    for category in CATEGORIES
}

globals().update(process_functions)
