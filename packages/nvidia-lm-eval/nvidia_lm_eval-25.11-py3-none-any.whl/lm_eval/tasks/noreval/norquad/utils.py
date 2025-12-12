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

import datasets
import transformers.data.metrics.squad_metrics as squad_metrics


def process_results(doc, results):
    preds = results[0]
    reference = doc["answers"]["text"][0]
    f1_sum = squad_metrics.compute_f1(reference, preds)
    exact_match = squad_metrics.compute_exact(reference, preds)
    return {"f1": f1_sum, "exact_match": exact_match}


def process_docs(dataset: datasets.Dataset):
    def _helper(doc):
        doc["title"] = doc["context"].strip().split("\n")[0].strip()
        doc["passage"] = "\n".join(doc["context"].strip().split("\n")[1:]).strip()
        doc["question"] = " ".join(doc["question"].strip().split())
        return doc

    return dataset.map(_helper)


def p0(doc):
    title = doc["title"]
    passage = doc["passage"]
    question = doc["question"]
    prompt = f"Tittel: {title}\n\nTekst: {passage}\n\nSpørsmål: {question}\n\nSvar:"
    return prompt


def p1(doc):
    title = doc["title"]
    passage = doc["passage"]
    question = doc["question"]
    prompt = f'Tittel: {title}\n\nTekst: {passage}\n\nGitt teksten over, hva er svaret på følgende spørsmål? "{question}"\n\nSvar:'
    return prompt


def p2(doc):
    title = doc["title"]
    passage = doc["passage"]
    question = doc["question"]
    prompt = (
        f"Tittel: {title}\n\nTekst: {passage}\n\nSvar på følgende: {question}\n\nSvar:"
    )
    return prompt


def p3(doc):
    title = doc["title"]
    passage = doc["passage"]
    question = doc["question"]
    prompt = f'Tittel: {title}\n\nTekst: {passage}\n\nHvordan kan man svare på spørsmålet "{question}", gitt teksten over?\n\nSvar:'
    return prompt


def p4(doc):
    title = doc["title"]
    passage = doc["passage"]
    question = doc["question"]
    prompt = f'Tittel: {title}\n\nTekst:{passage}\n\nGitt teksten over, besvar følgende spørsmål: "{question}"\n\nSvar:'
    return prompt
