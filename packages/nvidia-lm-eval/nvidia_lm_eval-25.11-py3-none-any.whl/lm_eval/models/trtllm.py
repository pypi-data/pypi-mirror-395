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
import logging
import copy
from typing import List, Optional, Tuple, Union

import torch
import torch.nn.functional as F
from tqdm import tqdm
from transformers import AutoTokenizer, BatchEncoding, T5Tokenizer

from lm_eval.models.utils import Collator
from lm_eval.api.model import NVLM
from lm_eval.api.registry import register_model


logger = logging.getLogger(__name__)

TokenSequence = Union[List[int], torch.LongTensor, torch.Tensor, BatchEncoding]

@register_model('trt-llm')
class TRTLLM(NVLM):
    def __init__(
        self,
        tokenizer: str,
        engine_dir: str,
        batch_size: int = 1,
        **kwargs,
    ):
        super().__init__()

        import tensorrt_llm
        from tensorrt_llm.runtime import ModelRunner

        assert isinstance(tokenizer, str)
        assert isinstance(engine_dir, str)

        self._batch_size = int(batch_size)
        self._max_gen_toks = 256

        self.tokenizer = self.get_tokenizer(tokenizer)
        self.runtime_rank = tensorrt_llm.mpi_rank()
        runner_kwargs = dict(engine_dir=engine_dir, rank=self.runtime_rank, **kwargs)
        self.runner = ModelRunner.from_dir(**runner_kwargs)
        logger.info("Loaded TRT-LLM engine")

    @staticmethod
    def get_tokenizer(tokenizer: str):
        try:
            tokenizer = AutoTokenizer.from_pretrained(tokenizer,
                                                      padding_side='left',
                                                      truncation_side='left',
                                                      trust_remote_code=True)
        except Exception:
            if not os.path.exists(tokenizer):
                raise ValueError(f"Tokenizer {tokenizer} does not exist")
            tokenizer = T5Tokenizer(tokenizer,
                                    padding_side='left',
                                    truncation_side='left',
                                    legacy=False)
        if tokenizer.pad_token_id is None:
            tokenizer.pad_token_id = tokenizer.eos_token_id
        return tokenizer

    @property
    def eot_token_id(self):
        try:
            return self.tokenizer.eos_id
        except AttributeError:
            return None

    @property
    def max_gen_toks(self):
        return self._max_gen_toks

    @property
    def max_length(self):
        raise NotImplementedError("TODO: add 'max_length' argument to TRTLLM model")

    @property
    def batch_size(self):
        return self._batch_size

    def tok_encode(self, string: str, max_length: Optional[int] = None):
        return self.tokenizer.encode(string, max_length=max_length, add_special_tokens=False)

    def tok_encode_batch(self, strings: List[str]) -> TokenSequence:
        return  [
            torch.IntTensor(self.tok_encode(s)) for s in strings
        ]

    def tok_decode(self, tokens):
        return self.tokenizer.batch_decode(tokens, skip_special_tokens=True)

    def _generate(self, input_tokens, max_tokens: int, until: List[str], **generation_kwargs: dict) -> dict:
        with torch.no_grad():
            outputs = self.runner.generate(
                input_tokens,
                max_new_tokens=max_tokens,
                end_id=self.tokenizer.eos_token_id,
                pad_id=self.tokenizer.pad_token_id,
                stop_words_list=until,
                return_dict=True,
                **generation_kwargs,
            )
        torch.cuda.synchronize()
        return outputs

    def generate_until(
        self, requests: List[Tuple[str, Union[List[str], str]]]
    ) -> List[str]:
        from tensorrt_llm.runtime import to_word_list_format
        def _collate(x):
            tokens = self.tok_encode(x[0])
            return len(tokens), x[0]

        def get_until(req_args):
            until = req_args.get('until', [])
            until = copy.deepcopy(until)  # prevent from modifying req_args for cache_key
            if '<|endoftext|>' not in until:
                until.append('<|endoftext|>')
            return until

        results = []

        re_ords = Collator([reg.args for reg in requests], sort_fn=_collate, group_by='gen_kwargs')
        chunks = re_ords.get_batched(n=self.batch_size, batch_fn=None)

        num_batches = len(re_ords) // self.batch_size

        for chunk in tqdm(
            chunks,
            total=num_batches,
            desc="TRTLLM.generate_until",
        ):
            request_args = chunk[0][1]
            max_gen_tokens = request_args.get("max_gen_toks", self.max_gen_toks)
            max_input_length = self.runner.max_seq_len - max_gen_tokens
            context = [torch.tensor(self.tok_encode(c[0], max_length=max_input_length), dtype=torch.int32) for c in chunk]
            context_lengths = [len(c) for c in context]
            until = get_until(request_args)
            # FIXME(martas): stop_words don't seem to work
            # stop_words_list = [until for _ in range(len(chunk))]
            # stop_words_list = to_word_list_format(stop_words_list, self.tokenizer)
            # stop_words_list = torch.Tensor(stop_words_list).to(torch.int32).to("cuda").contiguous()
            stop_words_list = None

            outputs = self._generate(
                context,
                max_gen_tokens,
                stop_words_list,
                # TODO(martas): can I safely pop from this dict instead of get in L116 and L118?
                **{k: v for k, v in request_args.items() if k not in ("until", "max_length")},
            )  # (batch_size, num_beams = 1)
            # shape: (batch, beams, tokens)
            assert outputs['output_ids'].shape[1] == 1, outputs['output_ids'].shape
            responses = []
            for request, out, c_len in zip(chunk, outputs['output_ids'], context_lengths):
                out = out[0][c_len:] # take first (and only) beam, and only tokens that were not part of a prompt
                out = self.tokenizer.decode(out)
                for stop in until:
                    out = out.split(stop)[0]
                responses.append(out)
            results.extend(responses)
            for request, response in zip(chunk, responses):
                self.cache_hook.add_partial("generate_until", request, response)

        logging.info(f"Finished generate_until for {len(requests)} requests.")

        return re_ords.get_original(results)

    def _loglikelihood_tokens(
        self,
        requests: List[Tuple[Tuple[str, str], TokenSequence, TokenSequence]],
        disable_tqdm: Optional[bool] = False,
    ) -> List[Tuple[float, bool]]:
        if not self.runner.gather_context_logits:
            raise RuntimeError('The provided trt-llm engine does not support context_logits. '
                               'Please build the engine with --gather_context_logits flag')
        results = []
        def _collate(x):
            tokens = self.tok_encode(x[0])
            return len(tokens), x[0]

        results = []
        re_ord = Collator(requests, sort_fn=_collate)
        chunks = re_ord.get_batched(n=self.batch_size, batch_fn=None)

        num_batches = len(re_ord) // self.batch_size

        for chunk in tqdm(
            chunks,
            total=num_batches,
            desc="TRTLLM._loglikelihood_tokens",
        ):
            cache_keys, inputs_tokens, targets_tokens = zip(*chunk)
            context = [torch.tensor(inp + tar, dtype=torch.int32) for inp, tar in zip(inputs_tokens, targets_tokens)]
            outputs = self._generate(context, 1, None)
            logits = outputs['context_logits']

            output_iterator = zip(
                cache_keys,
                logits,
                inputs_tokens,
                targets_tokens,
            )
            for cache_key, context_logits, input_tokens, target_tokens in output_iterator:
                # ligits[i] corresponds to tokens[i+1]
                log_softmax = F.log_softmax(context_logits[len(input_tokens)-1:-1], dim=-1).cpu()
                greedy_tokens = log_softmax.argmax(dim=-1)
                target_tokens = torch.tensor(target_tokens, dtype=torch.int64)
                max_equal = (greedy_tokens == target_tokens).all()
                target_logits = torch.gather(
                    log_softmax, 1, target_tokens.unsqueeze(-1)
                ).squeeze(-1)
                answer = (float(target_logits.sum()), bool(max_equal))
                results.append(answer)
                if cache_key is not None:
                    self.cache_hook.add_partial("loglikelihood", cache_key, answer)
        return re_ord.get_original(results)
