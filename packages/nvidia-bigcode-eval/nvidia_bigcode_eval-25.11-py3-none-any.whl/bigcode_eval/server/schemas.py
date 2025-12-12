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

"""Pydantic BaseModels schemas for server payload messages. 
Implements some names mapping between bigcode and openAI API schemas
"""

from pydantic import BaseModel, Field
from typing import Optional
from collections.abc import Iterable
from typing import TypedDict, List, Any
import random


class OpenAiRequestsParams(BaseModel):
    model: str = Field(alias="model", default=None)
    max_gen_toks: Optional[int] = Field(alias="max_tokens", default=None)
    until: Optional[list[str] | str] = Field(alias="stop", default=None)
    temperature: Optional[float | int] = None
    top_p: Optional[float] = None
    n: Optional[int] = None
    stream: Optional[bool] = None
    use_random_seed_in_requests: bool = Field(exclude=True, default=True)
    seed: Optional[int] = None

    class Config:
        populate_by_name = True

    def __init__(self, **data):
        super().__init__(**data)
        if self.use_random_seed_in_requests and self.seed is None:
            self.seed = random.randint(0, 2**32 - 1)


class OpenAiCompletionParams(OpenAiRequestsParams):
    prompt: Optional[str | list[str] | Iterable[int] | Iterable[Iterable[int]]]
    
    class Config:
        populate_by_name = True


class OpenAiChatCompletionParams(OpenAiRequestsParams):
    messages: Optional[list[dict[str, str]]]
    tools: list[dict] = None
    
    class Config:
        populate_by_name = True


class OpenAiOutputWithTools(TypedDict):
    text: Optional[str]
    tools: Optional[List[dict]]