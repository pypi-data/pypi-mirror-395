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
from lm_eval.api.registry import register_model
from lm_eval import utils

import httpx
from tqdm.asyncio import tqdm_asyncio
import asyncio
from lm_eval.models.nvcf import NVMixin
from transformers import LlamaTokenizerFast


@register_model('local')
class Local_Model(LM, NVMixin):
    def __init__(
            self,
            url,
            max_input_length,
            max_input_length_buffer=100,
            temperature=1e-5,
            top_p=1e-5,
            timeout=30,
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
        self._temperature = float(temperature)
        self.top_p = float(top_p)
        self._limit = asyncio.Semaphore(async_limit)
        self.max_input_length = max_input_length
        self.max_input_length_buffer = max_input_length_buffer

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
            tasks = [self.query_server(prompt, req_params) for prompt, req_params in requests]
            results = loop.run_until_complete(tqdm_asyncio.gather(*tasks))
        finally:
            loop.close()
    
        return results
    
    async def query_server(self, prompt, req_params):
        async with self._limit:
            request_json = self._construct_request(prompt=prompt, req_params=req_params)

            response = await self.client_post(request_json)
            
            continuation = self._process_response(response)

            for term in req_params.get('until', []):
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

    def _construct_request(self, prompt: str, req_params: dict):
        max_tokens = req_params.get('max_gen_toks', self.max_gen_toks)
        max_tokens = min(self.max_gen_toks, max_tokens)

        remaining_length = self.max_length - max_tokens - self.max_input_length_buffer
        encoded_prompt = self.tokenizer.encode(prompt)
        if len(encoded_prompt) > remaining_length:
            encoded_prompt = encoded_prompt[-remaining_length:]
            prompt = self.tokenizer.decode(encoded_prompt)

        messages = [{"content": prompt, "role": "user"}]
        request_json = {
            "model": "ensemble",
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": self.temperature,
            "top_p": self.top_p,
            "stream": False
        }
        return request_json

    def _process_response(self, response):
        json_resp = response.json()
        return json_resp["choices"][0]["message"]["content"]

    def loglikelihood(self, requests):
        raise NotImplementedError

    @property
    def max_gen_toks(self):
        return 256

    @property
    def temperature(self):
        return self._temperature

    @property
    def temperature(self):
        return self._temperature
