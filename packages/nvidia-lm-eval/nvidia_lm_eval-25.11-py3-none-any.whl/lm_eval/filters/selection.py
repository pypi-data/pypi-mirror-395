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

import warnings
from collections import Counter

from lm_eval.api.filter import Filter
from lm_eval.api.registry import register_filter


# TODO: implement "arg_max" filter. either it should take in an arbitrary "scoring"/reward function
# that takes an input and returns a scalar and then should select the max reward,
# or should implement different filters for different ways of handling a reward model's inference.


@register_filter("take_first")
class TakeFirstFilter(Filter):
    def __init__(self, fallback_value: str = "") -> None:
        """
        Can define custom behavior here, if an individual instantiation of a Filter class should have state.
        """
        self.fallback_value = fallback_value

    def apply(self, resps, docs):
        """
        Assuming each entry of `resps` is a list of model responses, we discard all but the first response.
        """
        def try_first(r):
            try:
                r = r[0]
            except:
                warnings.warn(
                    f"Failed to take the first element from {r}. Taking fallback value {self.fallback_value} ."
                )
                r = self.fallback_value
            return r
        return map(try_first, resps)


@register_filter("take_first_k")
class TakeKFilter(Filter):
    def __init__(self, **kwargs) -> None:
        self.k = kwargs.pop("k")

        super().__init__(**kwargs)

    def apply(self, resps, docs):
        # need resp to be subscriptable to check below
        resps = list(resps)
        # check we have at least k responses per doc, else we can't take the first k
        assert len(resps[0]) >= self.k, (
            f"Need at least {self.k} responses per doc to take first {self.k}, but got {len(resps[0])} only! Please increase TaskConfig.repeats ."
        )
        return map(lambda r: r[: self.k], resps)


@register_filter("majority_vote")
class MajorityVoteFilter(Filter):
    def __init__(self) -> None:
        """
        Can define custom behavior here, if an individual instantiation of a Filter class should have state.
        """

    def apply(self, resps, docs):
        """
        Each entry of `resps` is a list of model responses.
        We select the response that occurs most frequently in each entry of `resps`.
        """

        def select_majority(resp):
            counts = Counter(resp)
            vote = counts.most_common(1)[0][0]
            return vote

        return map(lambda r: [select_majority(r)], resps)
