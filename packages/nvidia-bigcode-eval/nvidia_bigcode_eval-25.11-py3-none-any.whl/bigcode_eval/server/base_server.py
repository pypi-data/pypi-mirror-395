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

import abc
import httpx
import pathlib
from typing import Optional
from tqdm.asyncio import tqdm_asyncio
import asyncio
from transformers import LlamaTokenizerFast
from pydantic import BaseModel
import logging
import os
from abc import abstractmethod
from bigcode_eval.server.openai_messages_handlers import BaseHandler

TOKENIZER_ASSETS = pathlib.Path(__file__).absolute().parent.parent / "llama_tokenizer"


class Server:
    def __init__(
            self,
            url,
            max_length,
            temperature=0.001,  # TODO: we want zero here
            top_p=0.95,
            timeout=30,
            async_limit=50,
            connection_retries=3,
            model_name: Optional[str] = None,
            **kwargs
    ):
        self.url = url
        transport = httpx.AsyncHTTPTransport(retries=connection_retries)
        self._client = httpx.AsyncClient(
            timeout=httpx.Timeout(timeout),
            transport=transport
        )
        self._limit = asyncio.Semaphore(async_limit)
        self.max_length = max_length
        self.temperature = temperature
        self.model_name = model_name
        self.top_p = top_p
        self._rank = 0
        self._world_size = 1
        self.tokenizer = LlamaTokenizerFast.from_pretrained(TOKENIZER_ASSETS)

    def generate(
            self,
            input_texts: list,
            max_gen_tokens: int,
            do_sample: bool,
            num_sequences: int,
            until = tuple(),
            gen_kwargs: Optional[dict[str, any]] = None,
        ) -> list:

        loop = asyncio.get_event_loop()
        if gen_kwargs is None:
            gen_kwargs = {}

        req_params = {
            "max_gen_toks": max_gen_tokens,
            "do_sample": do_sample,
            "temperature": self.temperature,
            "top_p": self.top_p,
            "use_random_seed_in_requests": num_sequences > 1
        }
        if self.model_name is not None:
            req_params["model"] = self.model_name

        if len(until) > 0:
            req_params["until"] = until

        tasks = [self.query_server(input_text, req_params, extra_req_params=gen_kwargs) for input_text in input_texts]
        results = loop.run_until_complete(tqdm_asyncio.gather(*tasks))
        return results
    
    @property
    def nvcf_token(self):
        return os.environ.get("NVCF_TOKEN")


    async def query_server(self, prompt, req_params, extra_req_params: dict[str, any] | None = None):
        async with self._limit:
            # TODO(martas) extract params renaming etc to a method so that child classes can adjust it

            max_tokens = req_params.get('max_gen_toks', self.max_gen_toks)
            until = req_params.get('until', []) 
            request_json = self._construct_request(prompt=prompt, req_params=req_params, extra_req_params=extra_req_params)
            logging.debug(f"Request json:\n {request_json}")
            response = await self.client_post(request_json)
            
            # prompt + continuation for completion continuation for chat
            response = self._process_response(response, prompt=prompt)

            for term in until:
                response = response.split(term)[0]

            logging.debug(f"Response:\n {response}")
            return response
    
    async def client_post(self, request_json):
        headers = {
            "Content-Type": "application/json",
            "accept": "application/json",
        }
        if self.nvcf_token:
            headers["Authorization"] = f"Bearer {self.nvcf_token}"

        response = await self._client.post(
            url=self.url,
            headers=headers,
            json=request_json,
        )
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as err:
            content = response.content.decode()
            raise RuntimeError(f"Request failed: {err}. Response content: {content}") from err

        return response
    
    @staticmethod
    def construct_payload_from_schema(model :BaseModel, req_params, extra_req_params: dict[str, any] | None = None):
        if extra_req_params is None:
            extra_req_params = {}
        payload = extra_req_params.copy()
        used_in_request_params = set(req_params.keys()).intersection(set(model.__fields__.keys()))
        logging.debug(f"Ignored request params: {set(req_params.keys()) - used_in_request_params}")
        payload.update(model(**{key: value for key, value in req_params.items() if key in used_in_request_params}).dict(exclude_unset=True, by_alias=True))
        return payload

    @abc.abstractmethod
    def _construct_request(self, prompt: str, req_params: dict) -> dict:
        raise NotImplementedError

    @abc.abstractmethod
    def _process_response(self, response, prompt: Optional[str | list[str]] = None) -> str:
        raise NotImplementedError

    def loglikelihood(self, requests):
        raise NotImplementedError

    def loglikelihood_rolling(self, requests):
        raise NotImplementedError

    @property
    def max_gen_toks(self):
        return 256    


class BaseOpenAiServer(Server):
    @property
    @abstractmethod
    def message_handler(self) -> BaseHandler:
        ...

    def _construct_request(self, prompt: str, req_params: dict, extra_req_params: dict[str, any] | None = None) -> dict:
        return self.message_handler._construct_request(prompt, req_params, extra_req_params=extra_req_params)

    def _process_response(self, response, prompt: Optional[str | list[str]] = None) -> str:
        return self.message_handler._process_response(response, prompt=prompt)
