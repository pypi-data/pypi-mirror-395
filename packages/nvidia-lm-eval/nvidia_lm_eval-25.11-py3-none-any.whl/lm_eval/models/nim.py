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
import asyncio
import httpx
from tqdm.asyncio import tqdm_asyncio
from os import environ

from lm_eval.api.registry import register_model
from lm_eval.models.server_base import Server

from tqdm.asyncio import tqdm_asyncio
import asyncio

@register_model('nim-completions')
class NIMCompletion(Server):
    def __init__(self, url, max_length, model_name: str = "ensemble", **kwargs):
        super().__init__(url, max_length, **kwargs)
        self.model_name = model_name

    def _construct_request(self, prompt: str, req_params: dict) -> dict:
        return {
            "model": self.model_name,
            "prompt": prompt,
            **req_params,  # TODO(martas): implement some params mapping if names don't match
        }
    
    def _process_response(self, response):
        json_resp = response.json()
        # TODO(martas): we might also have logprobs in json_resp["choices"][0]["logprobs"]["token_logprobs"]
        # TODO(martas): rigth now it's always [0.0,0.0]
        return json_resp["choices"][0]["text"]
    

@register_model('nim-chat-completions')
class NIMChat(Server):
    def __init__(self, url, max_length, model_name: str = "ensemble", **kwargs):
        super().__init__(url, max_length, **kwargs)
        self.model_name = model_name

    def _construct_request(self, prompt: str, req_params: dict) -> dict:
        return {
            "model": self.model_name,
            "messages": [{
                "content": prompt,
                "role": "user"
            }],
            **req_params,  # TODO(martas): implement some params mapping if names don't match
        }
    
    def _process_response(self, response):
        json_resp = response.json()
        return json_resp["choices"][0]["message"]["content"]


@register_model('nim-reward')
class NIMRewardModel(Server):
    def __init__(self, url, max_length, model_name: str = "RewardNIM", **kwargs):
        super().__init__(url, max_length, **kwargs)
        self.model_name = model_name

    def get_reward_score(self, requests):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            tasks = [self.query_server(req.doc['chat_messages']) for req in requests]
            results = loop.run_until_complete(tqdm_asyncio.gather(*tasks))
        finally:
            loop.close()
  
        return results
    
    async def query_server(self, chat_messages):
        async with self._limit:
            for message in chat_messages:
                message['content'] = self._truncate_content(message['content'], max_input_tokens=self.max_length)

            request_json = self._construct_request(chat_messages=chat_messages, req_params={})
            response = await self.client_post(request_json)
            continuation = self._process_response(response)

            return continuation
        
    def _truncate_content(self, prompt: str, max_input_tokens: int) -> str:
        encoded_prompt = self.tokenizer.encode(prompt)
        encoded_prompt_original_len = len(encoded_prompt)
        if encoded_prompt_original_len <= max_input_tokens:
            return prompt
        encoded_prompt = encoded_prompt[-max_input_tokens:]
        truncated_prompt = self.tokenizer.decode(encoded_prompt)
        print(f'WARNING: The content message was truncated. The conent length ({encoded_prompt_original_len}) exceeded {max_input_tokens} tokens.')
        print(f'Original prompt: {prompt}')
        print(f'Truncated prompt: {truncated_prompt}')
        return truncated_prompt
        
    async def client_post(self, request_json):
        response = await self._client.post(
            url=self.url,
            headers={
            "Content-Type": "application/json",
            "accept": "application/json",
            },
            json=request_json,
        )
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as err:
            content = response.content.decode()
            raise RuntimeError(f"Request failed: {err}. Response content: {content}") from err

        return response

    def _construct_request(self, chat_messages: list, req_params: dict) -> dict:
        for message in chat_messages:
            if sorted(list(message.keys())) != ['content', 'role']:
                raise ValueError('Each chat message needs to be a dictionary consisting of two keys: "content" and "role"')
        return {
            "model": self.model_name,
            "messages": chat_messages,
            **req_params,
        }
    
    def _process_response(self, response):
        json_resp = response.json()
        logprobs_content = json_resp["choices"][0]["message"]["content"]
        scores_per_category = {}
        for cat_to_score in logprobs_content.split(","):
            cat, score = cat_to_score.split(":")
            scores_per_category[cat] = float(score)
        return scores_per_category


@register_model('nim-multiturn-context')
class NIMChatMultiturnWithContext(Server):
    def __init__(self, url, max_length, model_name: str = "ensemble", **kwargs):
        super().__init__(url, max_length, **kwargs)
        self.model_name = model_name

    # This is a hacky model type supporting only chatrag_bench evaluation so far!
    def generate_until(self, requests):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            tasks = [self.query_server(req.doc["messages"], req.doc["ctxs"], req.args[1]) for req in requests]
            results = loop.run_until_complete(tqdm_asyncio.gather(*tasks))
        finally:
            loop.close()

        return results


    async def query_server(self, messages, context, req_params):
        async with self._limit:
            request_json = self._construct_request(messages=messages, context=context, req_params=req_params)

            response = await self.client_post(request_json)

            continuation = self._process_response(response)

            for term in req_params.get('until', []):
                continuation = continuation.split(term)[0]

            return continuation

    def _construct_request(self, messages: List[dict[str: str]], context: List[str], req_params: dict):
        max_tokens = req_params.get('max_gen_toks', self.max_gen_toks)
        max_tokens = min(self.max_gen_toks, max_tokens)

        context_messages = [{"role": "context", "content": chunk} for chunk in context]

        request_json = {
            "model": self.model_name,
            "messages": context_messages + messages,
            "max_tokens": max_tokens,
            "temperature": self.temperature,
            "top_p": self.top_p,
            "stream": False
        }

        return request_json

    def _process_response(self, response):
        json_resp = response.json()
        return json_resp["choices"][0]["message"]["content"]

    @property
    def max_gen_toks(self):
        return 512
