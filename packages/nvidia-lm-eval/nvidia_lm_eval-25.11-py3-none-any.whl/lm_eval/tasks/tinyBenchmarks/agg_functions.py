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

from typing import List

import numpy as np


try:
    import tinyBenchmarks as tb
except ModuleNotFoundError:
    raise ModuleNotFoundError(
        "`tinyBenchmarks` is required for tinyBenchmarks task metric calculation, install via \
`pip install git+https://github.com/felipemaiapolo/tinyBenchmarks`"
    )


def agg_pirt(items: List[float], benchmark: str) -> float:
    items = np.array(items)
    predictions = tb.evaluate(items, benchmark)
    return predictions[benchmark]["pirt"]


def agg_gpirt_arc(items: List[float], benchmark: str = "arc") -> float:
    items = np.array(items)
    predictions = tb.evaluate(items, benchmark)
    return predictions[benchmark]["gpirt"]


def agg_gpirt_gsm8k(items: List[float], benchmark: str = "gsm8k") -> float:
    items = np.array(items)
    predictions = tb.evaluate(items, benchmark)
    return predictions[benchmark]["gpirt"]


def agg_gpirt_hellaswag(items: List[float], benchmark: str = "hellaswag") -> float:
    items = np.array(items)
    predictions = tb.evaluate(items, benchmark)
    return predictions[benchmark]["gpirt"]


def agg_gpirt_mmlu(items: List[float], benchmark: str = "mmlu") -> float:
    items = np.array(items)
    predictions = tb.evaluate(items, benchmark)
    return predictions[benchmark]["gpirt"]


def agg_gpirt_truthfulqa(items: List[float], benchmark: str = "truthfulqa") -> float:
    items = np.array(items)
    predictions = tb.evaluate(items, benchmark)
    return predictions[benchmark]["gpirt"]


def agg_gpirt_winogrande(items: List[float], benchmark: str = "winogrande") -> float:
    items = np.array(items)
    predictions = tb.evaluate(items, benchmark)
    return predictions[benchmark]["gpirt"]
