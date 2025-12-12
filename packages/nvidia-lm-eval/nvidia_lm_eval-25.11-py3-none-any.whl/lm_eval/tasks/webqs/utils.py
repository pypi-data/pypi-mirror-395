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

from typing import Dict, List


def doc_to_choice(doc: Dict) -> List[str]:
    """Return all of the accepted answers as choices."""
    return _remove_prefixes(doc["answers"])


def doc_to_target(doc: Dict) -> List[int]:
    """Return list of indices of accepted answers (all of them)."""
    remaining = _remove_prefixes(doc["answers"])
    return list(range(len(remaining)))


def _remove_prefixes(aliases):
    """
    Remove any alias that has a strict prefix elsewhere in the list.

    This is an optimization. We can do this because if the prefix is acceptable by isgreedy,
    we can stop looking.
    """
    aliases.sort()
    ret = [aliases[0]]
    for alias in aliases[1:]:
        if not alias.startswith(ret[-1]):
            ret.append(alias)
    return ret
