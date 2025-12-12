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

import re

from lm_eval.tasks.meddialog.utils import doc_to_target_qsumm, doc_to_target_raw


def process_results_qsumm(doc, results):
    (loglikelihood,) = results
    _words = len(re.split(r"\s+", doc_to_target_qsumm(doc)))
    _bytes = len(doc_to_target_qsumm(doc).encode("utf-8"))
    return {
        "word_perplexity": (loglikelihood, _words),
        "byte_perplexity": (loglikelihood, _bytes),
        "bits_per_byte": (loglikelihood, _bytes),
    }


def process_results_raw(doc, results):
    (loglikelihood,) = results
    _words = len(re.split(r"\s+", doc_to_target_raw(doc)))
    _bytes = len(doc_to_target_raw(doc).encode("utf-8"))
    return {
        "word_perplexity": (loglikelihood, _words),
        "byte_perplexity": (loglikelihood, _bytes),
        "bits_per_byte": (loglikelihood, _bytes),
    }
