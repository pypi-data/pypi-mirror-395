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
from bfcl.model_handler.utils import retry_with_backoff
from openai import OpenAI, RateLimitError
from overrides import override


# For setup instructions, please refer to https://github.com/MeetKai/functionary for setup details.
class DeepSeekAPIHandler(OpenAIHandler):
    def __init__(self, model_name, temperature) -> None:
        super().__init__(model_name, temperature)
        self.model_style = ModelStyle.OpenAI
        self.is_fc_model = True
        self.client = OpenAI(
            base_url="https://api.deepseek.com", api_key=os.getenv("DEEPSEEK_API_KEY")
        )

    @retry_with_backoff(error_type=RateLimitError)
    def generate_with_backoff(self, **kwargs):
        """
        Per the DeepSeek API documentation:
        https://api-docs.deepseek.com/quick_start/rate_limit

        DeepSeek API does NOT constrain user's rate limit. We will try out best to serve every request.
        But please note that when our servers are under high traffic pressure, you may receive 429 (Rate Limit Reached) or 503 (Server Overloaded). When this happens, please wait for a while and retry.

        Thus, backoff is still useful for handling 429 and 503 errors.
        """
        start_time = time.time()
        api_response = self.client.chat.completions.create(**kwargs)
        end_time = time.time()

        return api_response, end_time - start_time

    @override
    def _query_FC(self, inference_data: dict):
        message: list[dict] = inference_data["message"]
        tools = inference_data["tools"]
        inference_data["inference_input_log"] = {"message": repr(message), "tools": tools}

        if len(tools) > 0:
            return self.generate_with_backoff(
                # The model name is always "deepseek-chat", as per https://api-docs.deepseek.com/quick_start/pricing
                # Note: Currently, it points to `DeepSeek-V3`
                model="deepseek-chat",
                messages=message,
                tools=tools,
            )
        else:
            return self.generate_with_backoff(
                model="deepseek-chat",
                messages=message,
            )
