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

import os
import time

from bfcl.model_handler.model_style import ModelStyle
from bfcl.model_handler.api_inference.openai import OpenAIHandler
from writerai import Writer


class WriterHandler(OpenAIHandler):
    def __init__(self, model_name, temperature) -> None:
        super().__init__(model_name, temperature)
        self.model_style = ModelStyle.WRITER
        self.client = Writer(api_key=os.getenv("WRITER_API_KEY"))
        self.is_fc_model = True

    #### FC methods ####

    def _query_FC(self, inference_data: dict):
        message: list[dict] = inference_data["message"]
        tools = inference_data["tools"]
        inference_data["inference_input_log"] = {"message": repr(message), "tools": tools}

        start_time = time.time()
        if len(tools) > 0:
            api_response = self.client.chat.chat(
                messages=message,
                model=self.model_name,
                temperature=self.temperature,
                tools=tools,
                tool_choice="auto",
            )
        else:
            api_response = self.client.chat.chat(
                messages=message,
                model=self.model_name,
                temperature=self.temperature,
            )
        end_time = time.time()

        return api_response, end_time - start_time
