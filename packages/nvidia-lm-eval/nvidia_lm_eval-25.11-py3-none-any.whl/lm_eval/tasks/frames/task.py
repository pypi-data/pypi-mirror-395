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

#Implementation based on: https://github.com/codelion/optillm/blob/main/scripts/eval_frames_benchmark.py

import datasets
import os
import pathlib
import openai
import re
import sys
from os import environ
from typing import Any, Dict, Optional
from transformers import AutoTokenizer

from lm_eval.api.instance import Instance
from lm_eval.api.task import ConfigurableTask
from lm_eval.api.metrics import mean
from lm_eval.tasks.frames.utils import preprocess_wikipedia_dataset, process_wiki_links_str, load_wikipedia_articles

class FramesTask(ConfigurableTask):
    VERSION = 0

    def __init__(
        self,
        config: Optional[dict] = None,
    ) -> None:
        if config is None:
            config = {}

        assert "strategy" in config, "Frames task must have a 'strategy' field in configuration."
        assert "judge" in config, "Frames task must have a 'judge' field in configuration."
        assert "max_request_tokens" in config, "Frames task must have a 'max_request_tokens' field in configuration."
        assert "tokenizer" in config, "Frames task must have a 'tokenizer' field in configuration."
        self.strategy = config["strategy"]
        assert self.strategy in ["naive", "naive_with_links", "oracle"]
        if self.strategy == 'oracle':
            assert "articles_type" in config, "Frames orcale task must have a 'articles_type' field in configuration."
            self.articles_type = config["articles_type"]

        self.judge = config["judge"]
        self.max_request_tokens = config["max_request_tokens"]
        self.tokenizer = AutoTokenizer.from_pretrained(config["tokenizer"])
        self.dataset = datasets.load_dataset("google/frames-benchmark", split="test")
        self.wiki_articles_path = os.path.join(pathlib.Path(__file__).parent.resolve(), "wikipedia_articles.json")

        # Check judge config
        judge_api_key_name = self.judge['api_key_env_name']
        if judge_api_key_name not in os.environ:
            raise EnvironmentError(
                f"Environment variable '{judge_api_key_name}' is not defined. "
                f"Please export your Judge API key as '{judge_api_key_name}' "
                f"(e.g., export {judge_api_key_name}=YOUR_API_KEY). "
                f"Judge details: URL - {self.judge['url']}, Model - {self.judge['name']}"
            )
            
        if self.strategy == 'oracle':
            if self.articles_type == 'raw':
                if not os.path.exists(self.wiki_articles_path):
                    print("Preprocessing Wikipedia dataset...")
                    preprocess_wikipedia_dataset(self.dataset, self.wiki_articles_path)
                    print(f"Preprocessing done, saved Wikipedia dataset to: {self.wiki_articles_path}")
                else:
                    print(f"Using existing preprocessed Wikipedia dataset: {self.wiki_articles_path}")
                self.wiki_texts_dict = load_wikipedia_articles(self.wiki_articles_path)
            elif self.articles_type == 'processed':
                self.frames_dataset = datasets.load_dataset("parasail-ai/frames-benchmark-wikipedia", split="train")
            else:
                raise NotImplementedError(f'Unsupported article type: {self.articles_type}.')

        super().__init__(
            config={
                "metadata": {"version": self.VERSION},
                "dataset_path": "google/frames-benchmark"
            }
        )

    def has_training_docs(self):
        return False

    def has_validation_docs(self):
        return False

    def has_test_docs(self):
        return True
    
    def test_docs(self):
        return self.dataset["test"]
    
    def get_full_prompt_text(self, doc):
        wiki_links_str = doc["wiki_links"]
        wiki_links = process_wiki_links_str(wiki_links_str)
        prompt = doc['Prompt']

        if self.strategy == 'naive':
            prompt_text = prompt
        elif self.strategy == 'naive_with_links':
            prompt_text = f"Here are the relevant Wikipedia articles:\n{wiki_links}\n\nBased on all the information, answer the query. \n\nQuery: {prompt}\n\n"
        elif self.strategy == 'oracle':
            wiki_texts = None
            if self.articles_type == 'raw':
                wiki_texts = [self.wiki_texts_dict[link] for link in wiki_links if link in self.wiki_texts_dict]
            elif self.articles_type == 'processed':
                wiki_texts = [self.frames_dataset.filter(lambda x: x['link'] == link)['text'][0] for link in wiki_links if link in self.frames_dataset['link']]

            wiki_text_str = "\n\n".join(wiki_texts)
            tokenized_wiki_text = self.tokenizer.encode(wiki_text_str, return_tensors='pt')
            tokenized_prompt = self.tokenizer.encode(f"Here are the relevant Wikipedia articles:\n\n\nBased on all the information, answer the query. \n\nQuery: {prompt}\n\n", return_tensors='pt')
            total_tokens = len(tokenized_wiki_text[0]) + len(tokenized_prompt[0])

            if self.max_request_tokens is not None and total_tokens > self.max_request_tokens:
                num_tokens_to_cut = total_tokens - self.max_request_tokens + 2048  # +2048 tokens buffer
                tokenized_wiki_text_to_cut = self.tokenizer.encode(wiki_text_str, return_tensors='pt')
                ids_list = tokenized_wiki_text_to_cut[0].tolist()[:len(tokenized_wiki_text_to_cut[0]) - num_tokens_to_cut]
                print(f"Warning: Token count exceeds the maximum request limit ({self.max_request_tokens}). Cutting from {total_tokens} to {len(ids_list)} tokens to prevent truncation errors.")
                cut_wiki_text = self.tokenizer.decode(ids_list, skip_special_tokens=True)
                wiki_text_str = f"{cut_wiki_text}..."  # add ellipsis to indicate cutting

            prompt_text = f"Here are the relevant Wikipedia articles:\n{wiki_text_str}\n\nBased on all the information, answer the query. \n\nQuery: {prompt}\n\n"
        else:
            raise NotImplementedError(f'Frames prompt does not support {self.strategy} strategy.')
        
        return prompt_text
    
    def doc_to_text(self, doc):
        return self.get_full_prompt_text(doc)

    def doc_to_target(self, doc):
        return doc["Answer"]
    
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
        temperature = self._config['generation_kwargs'].get('temperature', 0.0)
        return [
            Instance(
                request_type="generate_until",
                doc=doc,
                arguments=(ctx, {"temperature": temperature, 'until': []}),
                idx=0,
                **kwargs,
            )
        ]
    
    def process_results(self, doc, results):
        llm_response = results[0]
        dataset_index = doc["Unnamed: 0"]
        question = doc["Prompt"]
        ground_truth = doc["Answer"]
        evaluation_prompt = f"""===Task===
I need your help in evaluating an answer provided by an LLM against a ground
truth answer. Your task is to determine if the ground truth answer is present in the LLM's
response. Please analyze the provided data and make a decision.
===Instructions===
1. Carefully compare the "Predicted Answer" with the "Ground Truth Answer".
2. Consider the substance of the answers - look for equivalent information or correct answers.
Do not focus on exact wording unless the exact wording is crucial to the meaning.
3. Your final decision should be based on whether the meaning and the vital facts of the
"Ground Truth Answer" are present in the "Predicted Answer:"
===Input Data===
- Question: {question}
- Predicted Answer: {llm_response}
- Ground Truth Answer: {ground_truth}
===Output Format===
Provide your final evaluation in the following format:
"Explanation:" (How you made the decision?)
"Decision:" ("TRUE" or "FALSE" )
Please proceed with the evaluation."""
        
        judge_config = self.judge

        judge_client = openai.OpenAI(api_key=os.environ.get(judge_config['api_key_env_name']), base_url=judge_config['url'])
        evaluation_response = judge_client.chat.completions.create(
            model=judge_config["name"],
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": evaluation_prompt}
            ],
            max_tokens=judge_config["max_tokens"],
            stop=None,
            temperature=judge_config["temperature"],
        )

        evaluation_text = evaluation_response.choices[0].message.content.strip()

        # Remove the surrounding asterisks
        evaluation_text = re.sub(r"\*+", "", evaluation_text)

        # Extract the explanation
        explanation_match = re.search(r"Explanation:(.*?)Decision:", evaluation_text, re.DOTALL | re.IGNORECASE)
        if explanation_match:
            explanation = explanation_match.group(1).strip()
        else:
            explanation = ""

        # Extract the decision
        decision_match = re.search(r"Decision:\s*(\S+)", evaluation_text, re.IGNORECASE)
        if decision_match:
            decision = decision_match.group(1).upper()
        else:
            decision = "FALSE"

        print(f'**Processing: {dataset_index} item.**')
        print(f"**Question:**\n{question}")
        print(f"**Model response:**\n{llm_response}")
        print(f"**Ground truth:**\n{ground_truth}")
        print(f"**Judge explanation:**\n{explanation}")
        print(f"**Judge decision:**\n{decision}")
        print('----------------')

        return {
            "accuracy": 1 if decision == "TRUE" else 0,
        }

    def aggregation(self):
        """
        :returns: {str: [float] -> float}
            A dictionary where keys are the names of submetrics and values are
            functions that aggregate a list of metrics
        """
        return {
            "accuracy": mean
        }

    def higher_is_better(self):
        """
        :returns: {str: bool}
            A dictionary where keys are the names of submetrics and values are
            whether a higher value of the submetric is better
        """
        return {
            "accuracy": True,
        }
