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

import os
import pkg_resources
from typing import List, Tuple
from lm_eval.api.model import LM
from lm_eval.api.registry import register_model
from lm_eval import utils
import logging

import httpx
from tqdm.asyncio import tqdm_asyncio
import asyncio
from transformers import LlamaTokenizerFast

logger = logging.getLogger(__name__)

class NVMixin:
    pass


@register_model('nvcf')
class NVCF_Model(LM, NVMixin):

    _DEFAULT_MAX_LENGTH = 2048

    def __init__(
            self,
            function_id,
            function_version_id=None,  # by default, use prod version
            nvcf_url="https://api.nvcf.nvidia.com",
            max_length=None,
            max_input_length_buffer=400,
            temperature=1e-5,
            top_p=1e-5,
            timeout=120,
            async_limit=50,
            connection_retries=3,
            fetch_retries=5,
            new_token_retries=3,
            **kwargs
    ):

        super().__init__()

        nvcf_token = os.getenv("NVCF_TOKEN")
        jwt_token_provider = os.getenv("JWT_TOKEN_PROVIDER")
        ssa_client_id = os.getenv("NVCF_SSA_CLIENT_ID")
        ssa_client_secret = os.getenv("NVCF_SSA_CLIENT_SECRET")

        assert nvcf_token is not None or (jwt_token_provider is not None and
                                          ssa_client_id is not None and
                                          ssa_client_secret is not None), \
                                            "Pass token explicitly (export NVCF_TOKEN=...) or provide information for authentication"

        self._nvcf_url = nvcf_url
        self._function_id = function_id
        self._function_version_id = function_version_id
        self._jwt_token_provider = jwt_token_provider
        self._ssa_client_id = ssa_client_id
        self._ssa_client_secret = ssa_client_secret
        
        self._url = f'{self._nvcf_url.rstrip("/")}/v2/nvcf/pexec/functions/{self._function_id}'
        if function_version_id is not None:
            self._url = f"{self._url}/versions/{function_version_id}"

        if nvcf_token is None:
            nvcf_token = self._authenticate(
                jwt_token_provider=jwt_token_provider,
                ssa_client_id=ssa_client_id,
                ssa_client_secret=ssa_client_secret
            )
        transport = httpx.AsyncHTTPTransport(retries=connection_retries)
        self._client = httpx.AsyncClient(
            timeout=httpx.Timeout(timeout),
            transport=transport
        )
        self._token = nvcf_token
        self._is_refreshing_token = False
        self._refresh_token_event = asyncio.Event()
        self._refresh_token_event.set() # set to true
        self._temperature = float(temperature)
        self.top_p = float(top_p)
        self._limit = asyncio.Semaphore(async_limit)
        self._fetch_retries = fetch_retries
        self._new_token_retries = new_token_retries
        self._max_length = max_length
        self.max_input_length_buffer = max_input_length_buffer
        self.model_name = kwargs.get("model_name")

        #TODO do we want to use a tokenizer to estimate length?
        tokenizer_path = pkg_resources.resource_filename("lm_eval.models", "llama_tokenizer")
        self.tokenizer = LlamaTokenizerFast.from_pretrained(tokenizer_path)

    @classmethod
    def create_from_arg_string(cls, arg_string, additional_config=None):
        args = utils.simple_parse_args_string(arg_string)
        if additional_config:
            args['batch_size'] = additional_config.get('batch_size', 1)

        return cls(**args)

    @staticmethod
    def _authenticate(
            jwt_token_provider,
            ssa_client_id,
            ssa_client_secret
        ):
        with httpx.Client() as client:
            response = client.post(
                f'{jwt_token_provider.rstrip("/")}/token',
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                auth=httpx.BasicAuth(
                    username=ssa_client_id,
                    password=ssa_client_secret,
                ),
                data="scope=invoke_function&grant_type=client_credentials",
                timeout=60,
            )
            assert "access_token" in response.json(), "JWT not present in response..."
            token = response.json()["access_token"]
        return token

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
            request_json = self._construct_request(prompt=prompt, req_params=req_params)

            response = await self.client_post(request_json)
            response = await self.client_get(response)

            continuation = self._process_response(response)

            for term in req_params.get('until', []):
                continuation = continuation.split(term)[0]

            return continuation

    async def client_post(self, request_json):
        token_retries = 0
        while token_retries < self._new_token_retries:

            await self._refresh_token_event.wait()
            response = await self._client.post(
                url=self._url,
                headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self._token}",
                },
                json=request_json,
            )
            logger.info(f"Length: {self.count_tokens(request_json['messages'][0]['content'])}")
            if response.status_code == 401:
                await self.handle_401_error()
            else:
                try:
                    response.raise_for_status()
                except httpx.HTTPStatusError as err:
                    content = response.content.decode()
                    logger.error(f"Request: {request_json['messages'][0]['content']}")
                    logger.error(f"Length: {self.count_tokens(request_json['messages'][0]['content'])}")
                    raise RuntimeError(f"Request failed: {err}. Response content: {content}") from err
                break

            token_retries += 1

        return response

    async def client_get(self, response):
        token_retries = 0
        while token_retries < self._new_token_retries:
            fetch_retry_count = 0
            delay_seconds = 0.2
            multiplier = 1
            while response.status_code == 202 and fetch_retry_count <= self._fetch_retries:
                request_id = response.headers.get("NVCF-REQID")

                await self._refresh_token_event.wait()
                response = await self._client.get(
                    url=f'{self._nvcf_url.rstrip("/")}/v2/nvcf/pexec/status/{request_id}',
                    headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self._token}",
                    },
                )

                await asyncio.sleep(delay_seconds * multiplier)
                multiplier *= 2
                fetch_retry_count += 1

            if fetch_retry_count > self._fetch_retries:
                raise TimeoutError(f"Timeout error occurred: Couldn't get request from server after {self._fetch_retries} retries and {delay_seconds*multiplier} seconds.")

            if response.status_code == 401:
                await self.handle_401_error()
            else:
                try:
                    response.raise_for_status()
                except httpx.HTTPStatusError as err:
                    content = response.content.decode()
                    raise RuntimeError(f"Request failed: {err}. Response content: {content}") from err
                break

            token_retries += 1

        return response

    async def handle_401_error(self) -> None :
        """
        Async method to handle 401 errors.
        Blocks other threads from progressing elsewhere in the code using _refresh_token_event.
        Blocks other threads from re-validating with this function by using _is_refreshing_token

        Returns:
            None
        """
        if not self._is_refreshing_token:
            self._is_refreshing_token = True
            self._refresh_token_event.clear()
            try:
                await self.refresh_token()
            finally:
                self._is_refreshing_token = False
                self._refresh_token_event.set()
        else:
            await self._refresh_token_event.wait()

    async def refresh_token(self):
        print("401 Error - Refreshing Token")
        token = self._authenticate(
            self._jwt_token_provider,
            self._ssa_client_id,
            self._ssa_client_secret
        )
        self._token = token

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
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": self.temperature,
            "top_p": self.top_p,
            "stream": False
        }
        if self.model_name is not None:
            request_json["model"] = self.model_name
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

    def count_tokens(self, text):
        return len(self.tokenizer.encode(text))

    def loglikelihood_rolling(self, requests) -> List[Tuple[float]]:
        raise NotImplementedError("NVCF doesn't support loglikelihood.")
    
    @property
    def max_length(self):
        return self._max_length if self._max_length is not None else self._DEFAULT_MAX_LENGTH


@register_model('nvcf-multiturn-context')
class NVCFChatMultiturnWithContext(NVCF_Model):
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
            response = await self.client_get(response)

            continuation = self._process_response(response)

            for term in req_params.get('until', []):
                continuation = continuation.split(term)[0]

            return continuation
        
    def _construct_request(self, messages: List[dict[str: str]], context: List[str], req_params: dict):
        max_tokens = req_params.get('max_gen_toks', self.max_gen_toks)
        max_tokens = min(self.max_gen_toks, max_tokens)

        context_messages = [{"role": "context", "content": chunk} for chunk in context]

        request_json = {
            "messages": context_messages + messages,
            "max_tokens": max_tokens,
            "temperature": self.temperature,
            "top_p": self.top_p,
            "stream": False
        }

        return request_json
    
    @property
    def max_gen_toks(self):
        return 512