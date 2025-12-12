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

""" Classes for openAI chat completion and completion
messages handling, including payload creation and 
response postprocessing.
"""

import logging
import json
from pydantic import BaseModel
from abc import ABC, abstractmethod
from httpx import Response
from typing import Optional

from bigcode_eval.server.schemas import OpenAiChatCompletionParams, OpenAiCompletionParams, OpenAiOutputWithTools


class BaseHandler(ABC):
    @staticmethod
    def construct_payload_from_schema(model :BaseModel, req_params, extra_req_params: dict[str, any] | None = None):
        if extra_req_params is None:
            extra_req_params = {}
        payload = extra_req_params.copy()
        used_in_request_params = set(req_params.keys()).intersection(set(model.__fields__.keys()))
        logging.debug(f"Ignored params: {set(req_params.keys()) - used_in_request_params}")
        payload.update(model(**{key: value for key, value in req_params.items() if key in used_in_request_params}).dict(exclude_unset=True, by_alias=True))
        return payload
    
    @staticmethod
    @abstractmethod
    def _construct_request(prompt: str, req_params: dict, extra_req_params: dict[str, any] | None = None) -> dict:
        ...
    
    @staticmethod
    @abstractmethod
    def _process_response(response: Response) -> str:
        ...


class CompletionHandler(BaseHandler):
    @staticmethod
    def _construct_request(prompt: str, req_params: dict, extra_req_params: dict[str, any] | None = None) -> dict:
        return BaseHandler.construct_payload_from_schema(OpenAiCompletionParams, {"prompt": prompt, **req_params}, extra_req_params=extra_req_params)

    @staticmethod
    def _process_response(response: Response, prompt: Optional[str | list[str]] = None) -> str:
        json_resp = response.json()
        generation = json_resp["choices"][0]["text"]
        if prompt is not None:
            return prompt + generation
        return generation


class ChatCompletionHandler(BaseHandler):
    @staticmethod
    def _construct_request(prompt: str | list[dict] | OpenAiChatCompletionParams, req_params: dict, extra_req_params: dict = None) -> dict:
        
        if isinstance(prompt, str): 
            messages = [{
                "content": prompt,
                "role": "user"
            }]
        elif isinstance(prompt, list) and all(isinstance(item, dict) for item in prompt):
            messages = prompt

        elif isinstance(prompt, OpenAiChatCompletionParams):
            messages = prompt.messages
            if prompt.tools is not None:
                extra_req_params["tools"] = prompt.tools
                extra_req_params["nvext"] = {"guided_decoding_backend": "lm-format-enforcer"}

        else:
            raise ValueError("`prompt` must be either a string, list of dictionaries or OpenAiChatCompletionParams.")
        return BaseHandler.construct_payload_from_schema(
            OpenAiChatCompletionParams,
            {"messages": messages, **req_params},
            extra_req_params=extra_req_params
        )

    @staticmethod
    def _process_response(response: Response, prompt: Optional[str | list[str] | OpenAiChatCompletionParams] = None) -> str | OpenAiOutputWithTools:
        json_resp = response.json()
        text = json_resp["choices"][0]["message"]["content"]
        # if input contains tools we expect tools in output
        if isinstance(prompt, OpenAiChatCompletionParams) and prompt.tools is not None:
            tools = None
            if "tool_calls" in json_resp['choices'][0]["message"]:
                try:
                    tools = [
                        {func_call["function"]["name"]: json.loads(func_call["function"]["arguments"])}
                        for func_call in json_resp["choices"][0]["message"]["tool_calls"]
                    ]
                except:
                    logging.debug(f"Could not parse tool_calls: {json_resp['choices'][0]['message']['tool_calls']}")

            result = OpenAiOutputWithTools(text=text, tools=tools)
            return result
        return text
