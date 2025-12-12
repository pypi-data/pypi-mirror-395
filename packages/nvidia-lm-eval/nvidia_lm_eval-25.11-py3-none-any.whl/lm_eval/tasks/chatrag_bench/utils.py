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

# Code based on https://huggingface.co/datasets/nvidia/ChatRAG-Bench/blob/main/evaluation

import json
from typing import List

import pandas as pd
from pathlib import Path

from lm_eval.tasks.chatrag_bench.metrics import F1Metric

SYSTEM = "System: This is a chat between a user and an artificial intelligence assistant. The assistant gives helpful, detailed, and polite answers to the user's questions based on the context. The assistant should also indicate when the answer cannot be found in the context."

# Join double assistant answers
def process_messages(messages: List[dict[str, str]]):
    new_messages = []
    last_turn = ""
    for message in messages:
        if message["role"] == last_turn:
            new_messages[-1]["content"] = new_messages[-1]["content"] + " " + message["content"]
        else:
            last_turn = message["role"]
            new_messages.append(message)

    return new_messages
        


def process_docs_top5(dataset):
    dataset_path = Path(__file__).parent / "dataset"
    # TODO: propose a reasonable way to pass these files
    with open(dataset_path / "documents.json", "r") as f:
        docs = json.load(f)

    retrieved = pd.read_json(dataset_path / "nvidia_dragon_multiturn_retrieved.jsonl", orient="records")


    def _process(proc_doc, idx):
        ctx_nums = retrieved.iloc[idx]["ctxs"]
        ctx_docs = [docs[proc_doc["document"]][doc_id] for doc_id in ctx_nums]
        return {
            "ctxs": ctx_docs,
            "messages": process_messages(proc_doc["messages"]),
            "answers": proc_doc["answers"],
        }

    return dataset.map(_process, with_indices=True)


def process_docs_full(dataset):
    dataset_path = Path(__file__).parent / "dataset"
    # TODO: propose a reasonable way to pass these files
    with open(dataset_path / "documents.json", "r") as f:
        docs = json.load(f)

    def _process(proc_doc):
        return {
            "ctxs": docs[proc_doc["document"]],
            "messages": process_messages(proc_doc["messages"]),
            "answers": proc_doc["answers"],
        }

    return dataset.map(_process)


def reformat_question(turn_list) -> str:
    ## only take the latest 7 turns
    #turn_list = turn_list[-7:]
    assert turn_list[-1]['role'] == 'user'

    for item in turn_list:
        if item['role'] == 'user':
            ## only needs to add it on the first user turn
            item['content'] = 'Please give a full and complete answer for the question. ' + item['content']
            break
    
    question = ""
    for item in turn_list:
        if item["role"] == "user":
            question += "User: " + item["content"] + "\n\n"
        else:
            assert item["role"] == "assistant"
            question += "Assistant: " + item["content"] + "\n\n"
    
    question += "Assistant:"
    
    return question


def doc_to_text(doc):
    turn_list = doc['messages']
    question_formatted = reformat_question(turn_list)

    context = "\n\n".join(doc['ctxs'])
    model_input = SYSTEM + "\n\n" + context + "\n\n" + question_formatted

    return model_input


def doc_to_target(doc):
    return doc["answers"]


def parse_answer(answer):
    # NOTE: Everything is returned as a tuple for uniformity and hashability.
    if answer["number"] != "":
        return (str(answer["number"]),)
    if answer["spans"] != []:
        return tuple(answer["spans"])
    return (
        " ".join(
            [answer["date"]["day"], answer["date"]["month"], answer["date"]["year"]]
        ).strip(),
    )


def compute_f1_score(predicted_answers, groundtruth_answer):
    """Evaluating F1 Score"""
    if len(predicted_answers) != len(groundtruth_answer):
        groundtruth_answer = groundtruth_answer[:len(predicted_answers)]

    guess_list = []
    for guess in predicted_answers:
        guess = guess.strip()
        if "</s>" in guess:
            guess = guess.replace("</s>", "")
        guess_list.append(guess)

    answer_list = []
    for answer in groundtruth_answer:
        answer_list.append(answer)

    assert len(guess_list) == len(answer_list), \
        "lengths of guess and answer are different!"

    return F1Metric.compute_all_pairs(guess_list, answer_list)


def process_results(doc, results):
    preds, golds = results, doc["answers"]
    
    precision, recall, f1 = compute_f1_score(preds, golds)

    return {"precision": precision, "recall": recall, "f1": f1}
