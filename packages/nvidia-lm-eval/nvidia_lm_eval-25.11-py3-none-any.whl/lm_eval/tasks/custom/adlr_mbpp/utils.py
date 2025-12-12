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

import evaluate as hf_evaluate
from lm_eval.filters.sanitize import sanitize
from concurrent.futures import ThreadPoolExecutor


## run simple test to check code execution is enabled before model generation
# import os
# os.environ["HF_ALLOW_CODE_EVAL"] = "1"
# test_cases = ["assert add(2, 3)==5"]
# candidates = [["def add(a,b): return a+b\n\n"]]
# results = pass_at_k.compute(references=test_cases, predictions=candidates, k=[1])
# print(results)


## Evaluation functions
pass_at_k_fn = hf_evaluate.load("code_eval")


def pass_at_k(references, predictions, k: int):
    pass_at_k_results = pass_at_k_fn.compute(
        references=references,
        predictions=predictions,
        k=[k],
    )
    return pass_at_k_results[0][f"pass@{k}"]


def pass_at_1(references, predictions):
    return pass_at_k(references, predictions, k=1)


def pass_at_10(references, predictions):
    return pass_at_k(references, predictions, k=10)


## Formatting functions
def build_text(doc):
    description = doc["prompt"]
    test_example = doc["test_list"][0]
    prompt = f'"""\n{description}\n{test_example}\n"""\n'
    return prompt


def build_text_full_subset(doc):
    description = doc["text"]
    test_example = doc["test_list"][0]
    prompt = f'"""\n{description}\n{test_example}\n"""\n'
    return prompt


def build_references(doc):
    return "\n".join(doc["test_list"])


# NOTE(@ganler): MBPP+ extends the original MBPP jsonl data with a "test" field which
#                includes the testing code ready for execution. Note the "test" field
#                is different from HumanEval(+) which further requires a `check` func
MBBPPLUS_USE_MBPP_TESTS = 0  # bigcode-eval-harness default


def build_references_mbppplus(doc):
    if MBBPPLUS_USE_MBPP_TESTS == "1":
        return "\n".join(doc["test_list"])
    return "\n" + doc["test"]


def process_resp(resp):
    return [sanitize("\n" + r) for r in resp]


def build_predictions(resps, docs, num_workers=32):
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        results = list(executor.map(process_resp, resps))
    return results


def no_sanitize_predictions(resps, docs):
    preds = []
    for resp, doc in zip(resps, docs):
        pred = [r for r in resp]
        preds.append(pred)

    return preds


## Rewrite few-shot sampler to sample from `code` instead of the target (`test`)
from lm_eval.api.samplers import ContextSampler


class FewShotSampler(ContextSampler):
    # gen_prefix and instruction are unused, this sampler is a legacy file from ADLR.
    def get_context(self, doc, num_fewshot, gen_prefix: str = None, instruction: str = None):
        assert self.config.fewshot_split != self.config.test_split
        assert self.config.doc_to_choice is None

        # draw `n_samples` docs from fewshot_docs
        fewshot_examples = self.sample(num_fewshot)

        labeled_examples = ""
        for doc in fewshot_examples:
            doc_content = self.doc_to_text(doc)
            doc_target = doc["code"]
            labeled_examples += doc_content
            labeled_examples += self.target_delimiter
            labeled_examples += doc_target
            labeled_examples += self.fewshot_delimiter

        return labeled_examples
