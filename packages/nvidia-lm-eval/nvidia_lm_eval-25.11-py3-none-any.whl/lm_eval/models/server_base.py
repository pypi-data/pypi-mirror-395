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

import pkg_resources

from lm_eval.api.model import LM
from lm_eval import utils

import abc
import httpx
from tqdm.asyncio import tqdm_asyncio
import asyncio
from transformers import LlamaTokenizerFast


class Server(LM):
    def __init__(
            self,
            url,
            max_length,
            max_input_length_buffer=100,
            temperature=1e-5,
            top_p=1e-5,
            timeout=120,
            async_limit=50,
            connection_retries=3,
            **kwargs
    ):
        self.url = url
        transport = httpx.AsyncHTTPTransport(retries=connection_retries)
        self._client = httpx.AsyncClient(
            timeout=httpx.Timeout(timeout),
            transport=transport
        )
        self._limit = asyncio.Semaphore(async_limit)
        self.temperature = temperature
        self.top_p = top_p
        self.max_length = max_length
        self.max_input_length_buffer = max_input_length_buffer
        self._rank = 0
        self._world_size = 1

        tokenizer_path = pkg_resources.resource_filename("lm_eval.models", "llama_tokenizer")
        self.tokenizer = LlamaTokenizerFast.from_pretrained(tokenizer_path)

    @classmethod
    def create_from_arg_string(cls, arg_string, additional_config=None):
        args = utils.simple_parse_args_string(arg_string)
        if additional_config:
            args['batch_size'] = additional_config.get('batch_size', 1)

        return cls(**args)

    def generate_until(self, requests):

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            tasks = [self.query_server(req.args[0], req.args[1]) for req in requests]
            results = loop.run_until_complete(tqdm_asyncio.gather(*tasks))
        finally:
            loop.close()
    
        return results
    
    async def query_server(self, prompt, req_params):
        async with self._limit:

            # TODO(martas) extract params renaming etc to a method so that child classes can adjust it
            max_tokens = req_params.pop('max_gen_toks', self.max_gen_toks)
            until = req_params.pop('until', [])
            req_params["max_tokens"] = max_tokens
            req_params["temperature"] = self.temperature
            req_params["top_p"] = self.top_p
            do_sample = req_params.pop('do_sample', None)
            # if do_sample is not None:
            #     req_params['greedy'] = not do_sample
            prompt = self._truncate_prompt(prompt, max_gen_toks=max_tokens)
            request_json = self._construct_request(prompt=prompt, req_params=req_params)

            response = await self.client_post(request_json)
            
            continuation = self._process_response(response)

            for term in until:
                continuation = continuation.split(term)[0]

            return continuation
    
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

    def _truncate_prompt(self, prompt: str, max_gen_toks: int) -> str:
        remaining_length = self.max_length - max_gen_toks - self.max_input_length_buffer
        encoded_prompt = self.tokenizer.encode(prompt)
        if len(encoded_prompt) <= remaining_length:
            return prompt
        encoded_prompt = encoded_prompt[-remaining_length:]
        prompt = self.tokenizer.decode(encoded_prompt)
        # TODO(martas): should we warn here?
        return prompt

    @abc.abstractmethod
    def _construct_request(self, prompt: str, req_params: dict) -> dict:
        raise NotImplementedError

    @abc.abstractmethod
    def _process_response(self, response) -> str:
        raise NotImplementedError

    def loglikelihood(self, requests):
        raise NotImplementedError

    def loglikelihood_rolling(self, requests):
        raise NotImplementedError

    @property
    def max_gen_toks(self):
        return 256
