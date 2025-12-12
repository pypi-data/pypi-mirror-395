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

import importlib
import pathlib
import warnings
from copy import deepcopy

import filelock
import numpy as np
import torch
from tqdm import tqdm
from typing import List, Dict
from lm_eval.api.model import NVLM
from lm_eval.api.registry import register_model
from lm_eval.models.utils import Collator
from lm_eval.utils import simple_parse_args_string, eval_logger
from transformers import LlamaTokenizerFast


def _patch_pretrained_cfg(pretrained_cfg, trainer, tensor_model_parallel_size, pipeline_model_parallel_size):
    import omegaconf

    omegaconf.OmegaConf.set_struct(pretrained_cfg, True)
    with omegaconf.open_dict(pretrained_cfg):
        attributes_to_update = {
            "sequence_parallel": False,
            "activations_checkpoint_granularity": None,
            "activations_checkpoint_method": None,
            "precision": trainer.precision,
            "global_batch_size": None,
            "tensor_model_parallel_size": tensor_model_parallel_size,
            "pipeline_model_parallel_size": pipeline_model_parallel_size,
        }
        for name, value in attributes_to_update.items():
            if hasattr(pretrained_cfg, name):
                pretrained_cfg[name] = value
    return pretrained_cfg


def _get_target_from_class(target_class) -> str:
    return f"{target_class.__module__}.{target_class.__name__}"

def _get_model_cls(pretrained_cfg: dict):
    if 'target' in pretrained_cfg:
        target_cls = pretrained_cfg['target']
        print(f"Using model class: {target_cls}.")
        return target_cls
    else:
        raise KeyError("Required field 'target' (defining the model class) not present in the model config")


def load_model(model_path: str, trainer, tensor_model_parallel_size, pipeline_model_parallel_size) -> torch.nn.Module:
    from nemo.collections.nlp.models.language_modeling.megatron_gpt_model import \
        MegatronGPTModel
    from nemo.collections.nlp.parts.nlp_overrides import \
        NLPSaveRestoreConnector
    from nemo_aligner.models.nlp.gpt.megatron_gpt_regression_reward_model import \
        MegatronGPTRegressionRewardModel

    model_path = pathlib.Path(model_path)

    save_restore_connector = NLPSaveRestoreConnector()
    if model_path.is_dir():
        save_restore_connector.model_extracted_dir = model_path.as_posix()
    pretrained_cfg = save_restore_connector.restore_from(
        None, model_path.as_posix(), return_config=True, trainer=trainer
    )

    model_cls = _get_model_cls(pretrained_cfg)

    if not hasattr(pretrained_cfg, "target"):
        pretrained_cfg["target"] = _get_target_from_class(model_cls)

    pretrained_cfg = _patch_pretrained_cfg(
        pretrained_cfg, trainer,
        tensor_model_parallel_size=tensor_model_parallel_size,
        pipeline_model_parallel_size=pipeline_model_parallel_size,
    )
    model_to_load_path = model_path
    override_config = pretrained_cfg

    module_name, class_name = override_config.target.rsplit(".", 1)
    model_class = getattr(importlib.import_module(module_name), class_name)

    # monkeypatch _build_tokenizer method to be process-safe
    tokenizer_lock = filelock.FileLock(f"/tmp/{model_path.name}.tokenizer.lock")

    def _synced_build_tokenizer(self):
        with tokenizer_lock:
            self._original_build_tokenizer()

    model_class._original_build_tokenizer = model_class._build_tokenizer
    model_class._build_tokenizer = _synced_build_tokenizer

    model = model_class.restore_from(
        restore_path=model_to_load_path.as_posix(),
        trainer=trainer,
        override_config_path=override_config,
        save_restore_connector=save_restore_connector,
        map_location=f'cuda:{trainer.local_rank}',
    )

    model.freeze()
    model.training = False
    try:
        # Have to turn off activations_checkpoint_method for inference
        model.model.language_model.encoder.activations_checkpoint_method = None
    except AttributeError:
        pass
    return model


def setup_distributed_environment(trainer):
    from nemo.utils.app_state import AppState
    def dummy():
        return

    if trainer.strategy.launcher is not None:
        trainer.strategy.launcher.launch(dummy, trainer=trainer)
    trainer.strategy.setup_environment()

    app_state = AppState()

    return app_state

@register_model('nemo')
class NeMoGPT3LM(NVLM):

    def __init__(
            self,
            path,
            max_length=4096,
            batch_size=1,
            tensor_model_parallel_size=torch.cuda.device_count(),
            pipeline_model_parallel_size=1,
            precision="bf16",
            error_tolerance=0,
            add_bos_token: bool = False,
            template_filepath=None,
            max_new_tokens=256,
            **kwargs
        ):
        super().__init__()
        self.template_tokenizer = None
        if template_filepath:
            with open(template_filepath, 'r') as fp:
                template_override = fp.read()
                eval_logger.info(f"Template obtained from a file: \n {template_override}")
            # here LlamaTokenizerFast is only used to compile jinja template. In future, we can change it into a
            # dedicated jinja function. For now, we make sure compilation args are the same for HF and NeMo
            self.template_tokenizer = LlamaTokenizerFast.from_pretrained(
                pathlib.Path(__file__).parent / "llama_tokenizer"
            )
            self.template_tokenizer.chat_template = template_override
        from nemo.collections.nlp.parts.nlp_overrides import NLPDDPStrategy
        from pytorch_lightning.trainer.trainer import Trainer

        tensor_model_parallel_size = int(tensor_model_parallel_size)
        pipeline_model_parallel_size = int(pipeline_model_parallel_size)

        trainer = Trainer(
            strategy=NLPDDPStrategy(),
            devices=tensor_model_parallel_size,
            accelerator="gpu",
            num_nodes=pipeline_model_parallel_size,
            precision=precision,
            logger=False,
            enable_checkpointing=False,
            use_distributed_sampler=False,
        )

        self.model = load_model(
            path, trainer,
            tensor_model_parallel_size=tensor_model_parallel_size,
            pipeline_model_parallel_size=pipeline_model_parallel_size,
        ).cuda()
        self.tokenizer = self.model.tokenizer
        self.app_state = setup_distributed_environment(trainer)
        self.add_bos_token = add_bos_token

        self._max_length = max_length
        self._batch_size = int(batch_size)
        self._max_gen_toks = max_new_tokens

        error_tolerance = float(error_tolerance)
        assert 0 <= error_tolerance < 1
        self.error_tolerance = error_tolerance

    @classmethod
    def create_from_arg_string(cls, arg_string, additional_config=None):
        args = simple_parse_args_string(arg_string)
        if additional_config:
            args['batch_size'] = additional_config.get('batch_size', 1)

        return cls(**args)

    @property
    def eot_token_id(self):
        try:
            return self.tokenizer.eos_id
        except AttributeError:
            return None

    @property
    def max_length(self):
        return self._max_length

    @property
    def max_gen_toks(self):
        return self._max_gen_toks

    @property
    def batch_size(self):
        return self._batch_size

    def tok_encode(self, string: str):
        return self.tokenizer.text_to_ids(string)

    def tok_decode(self, tokens):
        return self.tokenizer.ids_to_text(tokens)

    def _loglikelihood_tokens(self, requests, disable_tqdm=False):
        from nemo.collections.nlp.modules.common.text_generation_utils import \
            generate

        res = []

        def _collate(x):
            toks = x[1] + x[2]
            return -len(toks), tuple(toks)

        re_ord = Collator(requests, sort_fn=_collate)
        chunks = re_ord.get_batched(n=self.batch_size, batch_fn=None)

        num_batches = len(re_ord) // self.batch_size
        num_errors_tolerance = int(round(self.error_tolerance * num_batches))
        num_errors = 0

        for chunk in tqdm(
            chunks,
            total=num_batches,
            disable=disable_tqdm,
            desc="NeMoGPT3LM._loglikelihood_tokens"
        ):
            inps = []
            ctxlens = []
            contlens = []

            for _, context_enc, continuation_enc in chunk:
                # Leave one token for generation. Tokens_to_generate = 0 breaks NeMo.
                inp = (context_enc + continuation_enc)[-(self.max_length-1):]

                ctxlen = len(context_enc) - max(
                    0, len(context_enc) + len(continuation_enc) - (self.max_length - 1)
                )
                ctxlens.append(ctxlen)
                contlens.append(len(continuation_enc))

                inps.append(self.tok_decode(inp))

            output = generate(
                self.model,
                inputs=inps,
                tokens_to_generate=1,
                min_tokens_to_generate=1,
                add_BOS=self.add_bos_token,
                compute_logprob=True,
                all_probs=True
            )

            first_token = 1 if self.add_bos_token else 0
            batch_token_ids = np.asarray(output['token_ids'])[:, first_token:-1]
            batch_logprobs = output['logprob'][:, first_token:-1].cpu().to(torch.float16).numpy()
            batch_full_logprob = output['full_logprob'][:, first_token:-1, :]

            # Compute greedy tokens for entire batch rather than calling it with proper ctxlen for each sample.
            # Additional tokens for each sample will be trimmed later.
            min_ctxlen = min(ctxlens)

            # Use min_ctxlen-1 instead of min_ctxlen since full_logprobs are not returns for the first token.
            batch_greedy_tokens = torch.argmax(batch_full_logprob[:, min_ctxlen-1:, :], -1).cpu().to(torch.float16).numpy()

            for token_ids, greedy_tokens, logprobs, ctxlen, contlen, (cache_key, _, _) in \
                    zip(batch_token_ids, batch_greedy_tokens, batch_logprobs, ctxlens, contlens, chunk):

                # Trim at contlen since shorter contexts in a batch will have more than one token generated.
                # Use ctxlen-1 instead of ctxlen same as for full_logprob in batch_greedy_tokens calculation
                logprobs = (logprobs[ctxlen-1:])[:contlen]
                try:
                    # NOTE(dfridman): logprobs is sometimes empty causing to fail on .tolist(). Why?
                    logprob = sum(logprobs)
                    continuation_tokens = (token_ids[ctxlen:])[:contlen]
                    len_diff = ctxlen - min_ctxlen
                    is_greedy = (continuation_tokens == (greedy_tokens[len_diff:])[:contlen]).all()
                    is_greedy = bool(is_greedy)

                    answer = (logprob, is_greedy)
                except Exception as e:
                    warnings.warn(f"Failed with: {str(e)}. Skipping.")
                    num_errors += 1
                    if num_errors > num_errors_tolerance:
                        raise e
                    answer = res[-1]  # NOTE(dfridman): reuse last prediction

                if cache_key is not None:
                    self.cache_hook.add_partial("loglikelihood", cache_key, answer)

                res.append(answer)

        return re_ord.get_original(res)

    def generate_until(self, requests):
        from nemo.collections.nlp.modules.common.text_generation_utils import \
            generate

        if not requests:
            return []
        res = []

        def get_until(req_args):
            until = req_args.get('until', [])
            until = deepcopy(until)  # prevent from modifying req_args for cache_key
            if '<|endoftext|>' not in until:
                until.append('<|endoftext|>')
            return until

        def _collate(x):
            toks = self.tok_encode(x[0])
            return len(toks), x[0]

        re_ords = Collator([reg.args for reg in requests], sort_fn=_collate, group_by='gen_kwargs')
        chunks = re_ords.get_batched(n=self.batch_size, batch_fn=None)
        for chunk in tqdm(
            chunks,
            total=len(re_ords) // self.batch_size,
            desc="NeMoGPT3LM.generate_until"
        ):
            contexts, all_gen_kwargs = zip(*chunk)
            # we assume all gen kwargs in the batch are the same
            # this is safe to assume because the `grouper` object ensures it.
            req_args = all_gen_kwargs[0]
            # unpack our keyword arguments.
            until = get_until(req_args)
            max_gen_toks = req_args.get('max_gen_toks', self.max_gen_toks)

            remaining_length = self.max_length - max_gen_toks
            if self.add_bos_token:
                remaining_length -= 1
            contexts = []
            for context, _ in chunk:
                encoded_context = self.tok_encode(context)
                encoded_context = encoded_context[-remaining_length:]
                contexts.append(
                    self.tok_decode(encoded_context)
                )

            output = generate(
                self.model,
                inputs=contexts,
                tokens_to_generate=max_gen_toks,
                add_BOS=self.add_bos_token,
                end_strings=until,
                greedy=True
            )

            answers = output['sentences']

            # TODO(jtomsia): there is a risk of trimming more or less tokens that desired
            # when doing it this way if special tokens appeared in context.
            # for now, don't know better solution for this.
            continuations = []
            for context, answer in zip(contexts, answers):
                continuations.append(
                    answer[len(context):]
                )

            for term in until:
                continuations = [
                    answer.split(term)[0] for answer in continuations
                ]

            for request, answer in zip(chunk, continuations):
                self.cache_hook.add_partial('generate_until', request, answer)
                res.append(answer)

        return re_ords.get_original(res)

    def get_reward_score(self, requests, disable_tqdm=False):
        if not requests:
            return []

        if self.batch_size != 1:
            #TODO implement support for processing batch size > 1
            raise ValueError('Function get_reward_score for nemo model does not currently support processing batch size > 1. Please set batch size to 1.')

        res = []

        def _collate(x):
            input_toks = self.tok_encode(x.doc['text'])
            return len(input_toks), input_toks

        self.model.prepare_for_inference()

        re_ord = Collator(requests, sort_fn=_collate)
        chunks = re_ord.get_batched(n=self.batch_size, batch_fn=None)
        num_batches = len(re_ord) // self.batch_size

        with torch.no_grad():
            for chunk in tqdm(
                chunks,
                total=num_batches,
                disable=disable_tqdm,
                desc="NeMoGPT3LM.get_reward_score"
            ):
                inps = []
                for instance in chunk:
                    inp = instance.doc['text']
                    inps.append(inp)

                outputs = self.model.infer(inps)

                for request, answer in zip(chunk, outputs):
                    result_tensor = answer[0][0]
                    # Multiply by the vector as advised by Nemo Reward Bench specification: https://huggingface.co/nvidia/Nemotron-4-340B-Reward
                    result_tensor = result_tensor * torch.tensor([0, 0, 0, 0, 0.3, 0.74, 0.46, 0.47, -0.33], device=result_tensor.device)
                    result_tensor = result_tensor.sum()

                    self.cache_hook.add_partial('get_reward_score', request.doc, result_tensor)
                    res.append(result_tensor)

        return re_ord.get_original(res)

    @property
    def chat_template(self) -> str:
            return self.template_tokenizer.chat_template

    @property
    def tokenizer_name(self) -> str:
        return self.template_tokenizer.name_or_path.replace("/", "__")

    def apply_chat_template(self, chat_history: List[Dict[str, str]]) -> str:
        """
        Method to apply a chat template to a list of chat history between user and model.
        Example how to call: lm-eval --task gsm8k --model nemo --model_args path=/home/tgrzegorzek/minitron-4b-v1-instruct.nemo,template_filepath=/home/tgrzegorzek/nemotron.template --write_out --apply_chat_template
        """
        if self.template_tokenizer is None:
            raise RuntimeError("Template filepath must be provided to instantiate template tokenizer")
        return self.template_tokenizer.apply_chat_template(
            chat_history, tokenize=False, add_generation_prompt=True
        )
