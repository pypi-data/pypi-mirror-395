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
import torch
from os import environ
from collections import defaultdict

from lm_eval.api.instance import Instance
from lm_eval.api.task import ConfigurableTask
from lm_eval.api.metrics import mean_exclude_none

# Currently supporting only Nemo models
# To make it work for NIM model you need to export the environmental variable `export REWARD_NIM=1`

# Chat template for Nemo model from https://github.com/NVIDIA/NeMo-Aligner/blob/main/examples/nlp/data/steerlm/common.py

SYSTEM_PROMPT = (
    "A chat between a curious user and an artificial intelligence assistant. "
    "The assistant gives helpful, detailed, and polite answers to the user's questions."
)

SYSTEM_PROMPT_TEMPLATE = "<extra_id_0>System\n{value}\n"

USER_TURN_TEMPLATE = "<extra_id_1>User\n{value}\n"

ASSISTANT_TURN_TEMPLATE = "<extra_id_1>Assistant\n{value}\n"

LABEL_PREFIX = "<extra_id_2>"

REWARD_SCORE_NEMO_WEIGHTS = {
    'helpfulness': 0.3,
    'correctness': 0.74,
    'coherence': 0.46,
    'complexity': 0.47,
    'verbosity': -0.33
}

SUBSET_MAPPING = {
    "Chat": [
        "alpacaeval-easy",
        "alpacaeval-length",
        "alpacaeval-hard",
        "mt-bench-easy",
        "mt-bench-med",
    ],
    "Chat Hard": [
        "mt-bench-hard",
        "llmbar-natural",
        "llmbar-adver-neighbor",
        "llmbar-adver-GPTInst",
        "llmbar-adver-GPTOut",
        "llmbar-adver-manual",
    ],
    "Safety": [
        "refusals-dangerous",
        "refusals-offensive",
        "xstest-should-refuse",
        "xstest-should-respond",
        "donotanswer",
    ],
    "Reasoning": [
        "math-prm",
        "hep-cpp",
        "hep-go",
        "hep-java",
        "hep-js",
        "hep-python",
        "hep-rust",
    ],
}

EXAMPLE_COUNTS = {
    "alpacaeval-easy": 100,
    "alpacaeval-length": 95,
    "alpacaeval-hard": 95,
    "mt-bench-easy": 28,
    "mt-bench-med": 40,
    "mt-bench-hard": 37,
    "math-prm": 984,  # actual length 447, upweighting to be equal to code
    "refusals-dangerous": 100,
    "refusals-offensive": 100,
    "llmbar-natural": 100,
    "llmbar-adver-neighbor": 134,
    "llmbar-adver-GPTInst": 92,
    "llmbar-adver-GPTOut": 47,
    "llmbar-adver-manual": 46,
    "xstest-should-refuse": 154,
    "xstest-should-respond": 250,
    "donotanswer": 136,
    "hep-cpp": 164,
    "hep-go": 164,
    "hep-java": 164,
    "hep-js": 164,
    "hep-python": 164,
    "hep-rust": 164,
}

def calculate_scores_per_section(example_counts, subset_mapping, metrics):
    """
    From: https://github.com/allenai/reward-bench/blob/main/rewardbench/utils.py
    Helper function for immediately logging RewardBench scores.
    """
    section_scores = {}
    for section, tests in subset_mapping.items():
        total_weighted_score = 0
        total_examples = 0
        for test in tests:
            if test in metrics:
                total_weighted_score += metrics[test] * example_counts[test]
                total_examples += example_counts[test]
        if total_examples > 0:
            section_scores[section] = total_weighted_score / total_examples
        else:
            section_scores[section] = 0
    return section_scores

class RewardBenchTask(ConfigurableTask):
    VERSION = 0
    DATASET_PATH = "allenai/reward-bench"
    DATASET_NAME = "default"
    DATASET_SPLIT = "filtered"

    def __init__(self):
        self.dataset_initialized = False
        super().__init__(config={"output_type": "get_reward_score", "task": "reward-bench", "metadata": {"version": self.VERSION}})
        self.model_results = {}

    def init_eval_dataset(self):
        def _modify_dataset(original_dataset):
            new_data = {
                'prompt': [],
                'answer': [],
                'test': [],
                'is_chosen': [],
                'id': [],
                'local_id': []
            }
            local_id = 0
            for row in original_dataset:
                question_id = row['id']
                prompt = row['prompt']
                test = row['subset']
                # Add data for the 'chosen' answer
                new_data['prompt'].append(prompt)
                new_data['answer'].append(row['chosen'])
                new_data['test'].append(test)
                new_data['is_chosen'].append(True)
                new_data['id'].append(question_id)
                new_data['local_id'].append(local_id)
                
                # Add data for the 'rejected' answer
                new_data['prompt'].append(prompt)
                new_data['answer'].append(row['rejected'])
                new_data['test'].append(test)
                new_data['is_chosen'].append(False)
                new_data['id'].append(question_id)
                new_data['local_id'].append(local_id)
                local_id += 1
            
            new_dataset = datasets.Dataset.from_dict(new_data)
            return new_dataset
        self.eval_dataset = _modify_dataset(self.dataset[self.DATASET_SPLIT])
        self.dataset_initialized = True

    def has_training_docs(self):
        return False

    def has_validation_docs(self):
        return False

    def has_test_docs(self):
        return True

    def test_docs(self):
        if not self.dataset_initialized:
            self.init_eval_dataset()
        return self.eval_dataset
    
    def get_chat_messages(self, doc) -> list:
        prompt = doc['prompt']
        answer = doc['answer']
        return [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": answer}
        ]
    
    def doc_to_text(self, doc):
        if environ.get('REWARD_NIM') is not None:
            return str(self.get_chat_messages(doc))
        else:
            text = SYSTEM_PROMPT_TEMPLATE.format(value=SYSTEM_PROMPT)
            text += USER_TURN_TEMPLATE.format(value=doc['prompt'])
            text += ASSISTANT_TURN_TEMPLATE.format(value=doc['answer'])
            text += LABEL_PREFIX
            return text

    def doc_to_target(self, doc):
        return doc["is_chosen"]
    
    def construct_requests(self, doc, ctx, **kwargs):
        """Uses RequestFactory to construct Requests and returns an iterable of
        Requests which will be sent to the LM.

        :param doc:
            The document as returned from training_docs, validation_docs, or test_docs.
        :param ctx: str
            The context string, generated by fewshot_context. This includes the natural
            language description, as well as the few shot examples, and the question
            part of the document for `doc`.
        """
        if environ.get('REWARD_NIM') is not None:
            doc['chat_messages'] = self.get_chat_messages(doc) # Add chat_messages that will be used by nim model
        else:
            doc['text'] = self.doc_to_text(doc) # Add text that will be used as an input for reward bench for nemo model

        return [
            Instance(
                request_type=self.OUTPUT_TYPE,
                doc=doc,
                arguments=(ctx, {}),
                idx=0,
                **kwargs,
            )
        ]
    
    def process_results(self, doc, results):
        question_id = doc['local_id']
        doc_test = doc['test']

        if len(results) != 1:
            raise ValueError(f"Expected result length to be 1, but got {len(result)}")
        
        result = results[0]
        
        if isinstance(result, torch.Tensor):
            result_score = result.item()
        else:
            result_score = 0.0                
            for score_name, score_weight in REWARD_SCORE_NEMO_WEIGHTS.items():
                result_score += result[score_name] * score_weight

        if question_id not in self.model_results:
            self.model_results[question_id] = {}

        if doc['is_chosen']:
            if 'chosen' in self.model_results[question_id]:
                raise KeyError(f"Key 'chosen' is not expected to be in the model_results for id: {question_id}.")
            self.model_results[question_id]['chosen'] = result_score
        else:
            if 'rejected' in self.model_results[question_id]:
                raise KeyError(f"Key 'rejected' is not expected to be in the model_results for id: {question_id}.")
            self.model_results[question_id]['rejected'] = result_score

        if 'chosen' in self.model_results[question_id] and 'rejected' in self.model_results[question_id]:
            chosen_score = self.model_results[question_id]['chosen']
            rejected_score = self.model_results[question_id]['rejected']
            pair_binary_score = chosen_score > rejected_score # Return binary score
            self.model_results[question_id]['pair_binary_score'] = pair_binary_score
            self.model_results[question_id]['test'] = doc_test
        else:
            pair_binary_score = None # Return None as we do not have all data to calculate the score

        return {'accuracy': pair_binary_score, f'accuracy_{doc_test}': pair_binary_score}

    def aggregation(self):
        """
        :returns: {str: [float] -> float}
            A dictionary where keys are the names of submetrics and values are
            functions that aggregate a list of metrics
        """
        submetric_function = {
            'accuracy': mean_exclude_none # accuracy
        }

        per_test_scores = defaultdict(list)
        for question_id in self.model_results:
            result = self.model_results[question_id]
            res_test = result['test']
            per_test_scores[res_test].append(result['pair_binary_score'])

        results_grouped = {}
        for test in EXAMPLE_COUNTS:
            submetric_function[f'accuracy_{test}'] = mean_exclude_none

            mean_acc = None
            if test in per_test_scores:
                mean_acc = sum(per_test_scores[test]) / len(per_test_scores[test])
            results_grouped[test] = mean_acc
            print(f'Accuracy for {test} test ({len(per_test_scores[test])} prompts): {mean_acc}')

        results_section = calculate_scores_per_section(EXAMPLE_COUNTS, SUBSET_MAPPING, results_grouped)
        print(f"Weighted accuracy per section: {results_section}")
        weighted_scores_per_section = list(results_section.values())
        leaderboard_score = sum(weighted_scores_per_section) / len(weighted_scores_per_section)

        print(f"Leaderboard score: {leaderboard_score}")
        
        return submetric_function
