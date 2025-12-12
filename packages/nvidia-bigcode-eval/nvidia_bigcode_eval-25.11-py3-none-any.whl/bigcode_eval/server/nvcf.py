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

"""
Base nvcf class, Nvcf completion and nvcf chat completion classes
"""
import httpx
import os
import logging
import asyncio
from typing import Optional
from bigcode_eval.server.base_server import BaseOpenAiServer
from bigcode_eval.server.openai_messages_handlers import ChatCompletionHandler, CompletionHandler

class BaseNVCF(BaseOpenAiServer):
    def __init__(
            self,
            max_length,
            temperature,
            function_id: str,
            function_version_id=None,
            base_url="https://api.nvcf.nvidia.com",
            max_new_tokens=1024,
            connection_retries=5,
            fetch_retries=100,
            async_limit=5,
            timeout=30,
            **kwargs,
    ):
        url = self.create_model_url(base_url, function_id, function_version_id=function_version_id)
        self.model_status_url = f"{base_url}/v2/nvcf/pexec/status/"
        self._fetch_retries = fetch_retries
        kwargs.update({
            "max_gen_toks": max_new_tokens,
            "temperature": temperature,
            "connection_retries": connection_retries,
            "async_limit": async_limit,
            "timeout": timeout,

        })
        kwargs.pop("url")
        super().__init__(url, max_length, **kwargs)

    @staticmethod
    def create_model_url(base_url: str, function_id: str, function_version_id: Optional[str] = None) -> str:
        model_url = f"{base_url}/v2/nvcf/pexec/functions/{function_id}"
        if function_version_id:
            model_url = f"{model_url}/versions/{function_version_id}"
        return  model_url
    
    @property
    def nvcf_token(self):
        return os.environ.get("NVCF_TOKEN")
    

    async def query_server(self, prompt, req_params, extra_req_params: dict[str, any] | None = None):
        async with self._limit:
            max_tokens = req_params.get('max_gen_toks', self.max_gen_toks)
            until = req_params.get('until', [])
            if isinstance(prompt, str):
                prompt = self._truncate_prompt(prompt, max_gen_toks=max_tokens)
            request_json = self._construct_request(prompt, req_params, extra_req_params=extra_req_params)
            logging.debug(f"Request json: {request_json}")
            response = await self.client_post(request_json)
            response = await self.client_get(response)

            # prompt + continuation for completion continuation for chat
            response = self._process_response(response, prompt=prompt)

            for term in until:
                response = response.split(term)[0]

            if logging.getLogger().isEnabledFor(logging.DEBUG):
                logging.debug(f"Request json: {request_json}")
                logging.debug(f"Response:\n {response}")
            return response


    async def client_get(self, response):
        fetch_retry_count = 0
        delay_seconds = 0.2
        multiplier = 1
        while response.status_code == 202 and fetch_retry_count <= self._fetch_retries:
            request_id = response.headers.get("NVCF-REQID")

            response = await self._client.get(
                url=f'{self.model_status_url}/{request_id}',
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.nvcf_token}",
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

        return response



class NVCFCompletion(BaseNVCF):
    @property
    def message_handler(self):
        return CompletionHandler
    

class NVCFChat(BaseNVCF):
    @property
    def message_handler(self):
        return ChatCompletionHandler