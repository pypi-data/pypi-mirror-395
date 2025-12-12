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

import functools
import logging
import os
from lm_eval.api.model import NVLM
from lm_eval.api.registry import register_model
from lm_eval.models.utils import Collator
from lm_eval.utils import simple_parse_args_string
from tqdm import tqdm

import torch
import torch.nn.functional as F

def model_provider(cfg, pre_process=True, post_process=True):
    from megatron.core.models.gpt.gpt_layer_specs import get_gpt_layer_with_transformer_engine_spec
    from megatron.core.models.gpt import GPTModel
    from megatron.training import get_args
    from megatron.training.arguments import core_transformer_config_from_args
    
    args = get_args()
    config = core_transformer_config_from_args(get_args())

    if args.spec is not None:
        transformer_layer_spec = import_module(args.spec)
    else:
        transformer_layer_spec = get_gpt_layer_with_transformer_engine_spec(args.num_experts, args.moe_grouped_gemm)

    model = GPTModel(
        config=config,
        transformer_layer_spec=transformer_layer_spec,
        vocab_size=args.padded_vocab_size,
        max_sequence_length=args.max_position_embeddings,
        pre_process=pre_process,
        post_process=post_process,
        fp16_lm_cross_entropy=args.fp16_lm_cross_entropy,
        parallel_output=False,
        share_embeddings_and_output_weights=not args.untie_embeddings_and_output_weights,
        position_embedding_type=args.position_embedding_type,
        rotary_percent=args.rotary_percent,
    )
    return model

def get_result_megatron(response, ctxlen, continuation_enc, logits):
    """Process results from OpenAI API response.

    :param response: dict
        OpenAI API Response
    :param ctxlen: int
        Length of context (so we can slice them away and only keep the predictions)
    :return:
        continuation_logprobs: np.array
            Log probabilities of continuation tokens
        is_greedy: bool
            whether argmax matches given continuation exactly
    """
    logprobs = response
    continuation_logprobs = sum(logprobs[ctxlen-1:])

    if logits != []:
        logits_softmax = F.log_softmax(logits, dim=1)

        greedy_tokens = logits_softmax[ctxlen-1:-1].argmax(dim=-1).cpu()
        continuation_enc = torch.LongTensor(continuation_enc)

        is_greedy = (greedy_tokens == continuation_enc).all()
    else:
        is_greedy = True
    return continuation_logprobs, is_greedy

@register_model('megatron')
class MegatronGPT3LM(NVLM):

    def __init__(self):
        """

        :param engine: str
            OpenAI API engine (e.g. davinci)
        :param truncate: bool
            Truncate input if too long (if False and input is too long, throw error)
        """
        super().__init__()

        from megatron.training import get_args, get_tokenizer
        from megatron.training.arguments import core_transformer_config_from_args
        from megatron.training.checkpointing import load_checkpoint
        from megatron.training import get_model

        self.args = get_args()
        config = core_transformer_config_from_args(self.args)
        self.model = get_model(functools.partial(model_provider, config), wrap_with_ddp=False)
        if self.args.load is not None:
            if not os.path.exists(self.args.load):
                raise ValueError(f"Checkpoint dir {self.args.load} does not exist")
            _ = load_checkpoint(self.model, None, None)

        assert len(self.model) == 1, "Above condition should have caught this"
        self.model = self.model[0]

        self.tokenizer = get_tokenizer()
        self.vocab_size = self.tokenizer.vocab_size

        self.max_gen_tokens = 256

    @classmethod
    def create_from_arg_string(cls, arg_string, additional_config=None):
        args = simple_parse_args_string(arg_string)
        return cls(**args)

    @property
    def eot_token_id(self):
        return self.tokenizer.eos_token_id

    @property
    def max_length(self):
        return self.args.seq_length

    @property
    def max_gen_toks(self):
        return self.max_gen_tokens

    @property
    def batch_size(self):
        return self.args.micro_batch_size

    @property
    def device(self):
        # Isn't used because we override _loglikelihood_tokens
        raise NotImplementedError()

    def tok_encode(self, string: str):
        return self.tokenizer.tokenize(string)

    def tok_decode(self, tokens):
        return self.tokenizer.detokenize(tokens)

    def _loglikelihood_tokens(self, requests, disable_tqdm=False):
        from megatron.inference.text_generation import generate_and_post_process
        res = []

        def _collate(x):
            # this doesn't efficiently handle last-token differences yet, but those are kinda annoying because
            # it's not guaranteed that the 100 or so logprobs we get to see actually contain all the continuations
            # we care about and so we need some kind of backup for when it isn't
            toks = x[1] + x[2]
            return -len(toks), tuple(toks)

        re_ord = Collator(requests, sort_fn=_collate)
        chunks = re_ord.get_batched(n=self.batch_size, batch_fn=None)

        for chunk in tqdm(chunks, disable=disable_tqdm):
            inps = []
            ctxlens = []
            gen_outs = []
            logits_outs = []

            for cache_key, context_enc, continuation_enc in chunk:
                inp = (context_enc + continuation_enc)[-(self.max_length-5):]

                # TODO: the logic is much simpler if we just look at the length of continuation tokens
                ctxlen = len(context_enc) - max(
                    0, len(context_enc) + len(continuation_enc) - (self.max_length - 5)
                )
                inps.append(self.tokenizer.detokenize(inp))
                ctxlens.append(ctxlen)

            _, _, output_log_probs, _, logits = generate_and_post_process(
                    self.model,
                    prompts=inps,
                    tokens_to_generate=0,
                    return_output_log_probs=True,
                    return_logits=True
                    )
            gen_outs.extend(output_log_probs)
            logits_outs.extend(logits)

            for resp, logits, ctxlen, (cache_key, context_enc, continuation_enc) in zip(
                gen_outs, logits_outs, ctxlens, chunk
            ):
                # TODO: this will disable is_greedy calculation and always return True.
                # Potential solution is to add request arguments to loglikelihood (the same way generate_until processes
                # them) and set 'need_greedy' flag there
                logits = []

                answer = get_result_megatron(resp, ctxlen, continuation_enc, logits)

                res.append(answer)

                # partial caching
                if cache_key is not None:
                    self.cache_hook.add_partial("loglikelihood", cache_key, answer)

        return re_ord.get_original(res)

    def generate_until(self, requests):
        from megatron.inference.text_generation import generate_and_post_process

        if not requests:
            return []
        res = []

        def get_until(req_args):
            return req_args.get('until', [])

        def _collate(x):
            toks = self.tok_encode(x[0])
            return len(toks), x[0]

        re_ords = Collator([reg.args for reg in requests], sort_fn=_collate, group_by='gen_kwargs')
        chunks = re_ords.get_batched(n=self.batch_size, batch_fn=None)
        # TODO(martas): is there a way to warn only once? adding WAR for now
        warned = False
        for chunk in chunks:
            contexts, all_gen_kwargs = zip(*chunk)
            # we assume all gen kwargs in the batch are the same
            # this is safe to assume because the `grouper` object ensures it.
            req_args = all_gen_kwargs[0]

            until = get_until(req_args)
            max_gen_toks = req_args.get('max_gen_toks', self.max_gen_toks)
            if len(until) > 0 and not warned:
                warned = True
                logging.warning("Stop words are currently not supported for Megatron generate_until type requests as "
                                "stopping criteria. They will be trimmed in postprocessing")

            # Don't know why we need -1 but megatron breaks otherwise
            remaining_length = self.max_length - max_gen_toks - 1
            contexts = []
            for context, _ in chunk:
                encoded_context = self.tok_encode(context)
                encoded_context = encoded_context[-remaining_length:]
                contexts.append(
                    self.tok_decode(encoded_context)
                )

            prompts_plus_generations, *_ = generate_and_post_process(
                self.model,
                prompts=contexts,
                tokens_to_generate=max_gen_toks,
                top_k_sampling=1,
                top_p_sampling=0.0,
            )
            answers = [
                generation[len(context):] for context, generation in zip(contexts, prompts_plus_generations)
            ]

            for term in until:
                answers = [
                    answer.split(term)[0] for answer in answers
                ]

            for request, answer in zip(chunk, answers):
                self.cache_hook.add_partial('generate_until', request, answer)
                res.append(answer)

        return re_ords.get_original(res)

    def _model_call(self, inps):
        # Isn't used because we override _loglikelihood_tokens
        raise NotImplementedError()

    def _model_generate(self, context, max_length, eos_token_id):
        # Isn't used because we override generate_until
        raise NotImplementedError()
