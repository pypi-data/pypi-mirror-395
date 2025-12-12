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

import itertools
import logging
from typing import Generator

import datasets

from lm_eval.tasks.ruler.common_utils import DEFAULT_SEQ_LENGTHS, get_tokenizer
from lm_eval.tasks.ruler.prepare_niah import generate_samples, get_haystack


TEMPLATE = """Some special magic {type_needle_v} are hidden within the following text. Make sure to memorize it. I will quiz you about the {type_needle_v} afterwards.\n{context}\nWhat are all the special magic {type_needle_v} for {query} mentioned in the provided text?"""
eval_logger = logging.getLogger(__name__)


def download_dataset(df: Generator) -> dict[str, datasets.Dataset]:
    return {
        "test": datasets.Dataset.from_list(
            list(itertools.chain.from_iterable(df)), split=datasets.Split.TEST
        )
    }


def niah_single_1(**kwargs):
    seq_lengths = kwargs.pop("max_seq_lengths", DEFAULT_SEQ_LENGTHS)
    return download_dataset(
        generate_samples(
            get_haystack(type_haystack="repeat"),
            max_seq_length=seq,
            template=TEMPLATE,
            type_haystack="repeat",
            type_needle_k="words",
            type_needle_v="numbers",
            num_samples=500,
            TOKENIZER=get_tokenizer(**kwargs),
        )
        for seq in seq_lengths
    )


def niah_single_2(**kwargs):
    seq_lengths = kwargs.pop("max_seq_lengths", DEFAULT_SEQ_LENGTHS)
    return download_dataset(
        generate_samples(
            get_haystack(type_haystack="essay"),
            max_seq_length=seq,
            template=TEMPLATE,
            type_haystack="essay",
            type_needle_k="words",
            type_needle_v="numbers",
            num_samples=500,
            TOKENIZER=get_tokenizer(**kwargs),
        )
        for seq in seq_lengths
    )


def niah_single_3(**kwargs):
    seq_lengths = kwargs.pop("max_seq_lengths", DEFAULT_SEQ_LENGTHS)
    return download_dataset(
        generate_samples(
            get_haystack(type_haystack="essay"),
            max_seq_length=seq,
            template=TEMPLATE,
            type_haystack="essay",
            type_needle_k="words",
            type_needle_v="uuids",
            num_samples=500,
            TOKENIZER=get_tokenizer(**kwargs),
        )
        for seq in seq_lengths
    )


def niah_multikey_1(**kwargs):
    seq_lengths = kwargs.pop("max_seq_lengths", DEFAULT_SEQ_LENGTHS)
    return download_dataset(
        generate_samples(
            get_haystack(type_haystack="essay"),
            max_seq_length=seq,
            template=TEMPLATE,
            type_haystack="essay",
            type_needle_k="words",
            type_needle_v="numbers",
            num_needle_k=4,
            num_samples=500,
            TOKENIZER=get_tokenizer(**kwargs),
        )
        for seq in seq_lengths
    )


def niah_multikey_2(**kwargs):
    seq_lengths = kwargs.pop("max_seq_lengths", DEFAULT_SEQ_LENGTHS)
    return download_dataset(
        generate_samples(
            get_haystack(type_haystack="needle"),
            max_seq_length=seq,
            template=TEMPLATE,
            type_haystack="needle",
            type_needle_k="words",
            type_needle_v="numbers",
            num_samples=500,
            TOKENIZER=get_tokenizer(**kwargs),
        )
        for seq in seq_lengths
    )


def niah_multikey_3(**kwargs):
    seq_lengths = kwargs.pop("max_seq_lengths", DEFAULT_SEQ_LENGTHS)
    return download_dataset(
        generate_samples(
            get_haystack(type_haystack="needle"),
            max_seq_length=seq,
            template=TEMPLATE,
            type_haystack="needle",
            type_needle_k="uuids",
            type_needle_v="uuids",
            num_samples=500,
            TOKENIZER=get_tokenizer(**kwargs),
        )
        for seq in seq_lengths
    )


def niah_multivalue(**kwargs):
    seq_lengths = kwargs.pop("max_seq_lengths", DEFAULT_SEQ_LENGTHS)
    return download_dataset(
        generate_samples(
            get_haystack(type_haystack="essay"),
            max_seq_length=seq,
            template=TEMPLATE,
            type_haystack="essay",
            type_needle_k="words",
            type_needle_v="numbers",
            num_needle_v=4,
            num_samples=500,
            TOKENIZER=get_tokenizer(**kwargs),
        )
        for seq in seq_lengths
    )


def niah_multiquery(**kwargs):
    seq_lengths = kwargs.pop("max_seq_lengths", DEFAULT_SEQ_LENGTHS)
    return download_dataset(
        generate_samples(
            get_haystack(type_haystack="essay"),
            max_seq_length=seq,
            template=TEMPLATE,
            type_haystack="essay",
            type_needle_k="words",
            type_needle_v="numbers",
            num_needle_q=4,
            num_samples=500,
            TOKENIZER=get_tokenizer(**kwargs),
        )
        for seq in seq_lengths
    )
