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

# Original Copyright UC Berkeley.
# For the original license and copyright information, see the LICENSE file in this repository.

from typing import Dict, List, Any, Literal
from pydantic import BaseModel, model_validator


class FunctionParameters(BaseModel):
    type: str
    properties: Dict[str, Dict[str, Any]]
    required: List[str]


class Function(BaseModel):
    name: str
    description: str
    parameters: FunctionParameters


class Tool(BaseModel):
    type: str
    function: Function


class Message(BaseModel):
    # Restrict role to only valid values
    role: Literal["user", "system", "assistant"]
    content: str


class OpenAIFormatData(BaseModel):
    """
    Represents the structure of the OpenAI format data.json file.
    """

    messages: List[List[Message]]
    tools: List[Tool]
    tool_calls_ground_truth: List[Dict[str, Dict[str, Any]]]

    # Model validators to ensure lists are not empty
    @model_validator(mode="after")
    def validate_non_empty_lists(self) -> "OpenAIFormatData":
        if not self.messages:
            raise ValueError("messages cannot be empty")
        if not self.tools:
            raise ValueError("tools cannot be empty")
        if not self.tool_calls_ground_truth:
            raise ValueError("tool_calls_ground_truth cannot be empty")
        return self


class NativeFormatQuestionData(BaseModel):
    """
    Represents the structure of the native format data.json file.
    """

    id: str
    question: List[List[Message]]
    function: List[Function]

    @model_validator(mode="after")
    def validate_non_empty_lists(self) -> "NativeFormatQuestionData":
        if not self.question:
            raise ValueError("question cannot be empty")
        if not self.function:
            raise ValueError("function cannot be empty")
        return self


class NativeFormatGroundTruthData(BaseModel):
    """
    Represents the structure of the native format ground truth data.json file.
    """

    id: str
    ground_truth: List[Dict[str, Dict[str, Any]]]

    @model_validator(mode="after")
    def validate_non_empty_lists(self) -> "NativeFormatGroundTruthData":
        if not self.ground_truth:
            raise ValueError("ground_truth cannot be empty")
        return self
