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

import json
import time

import requests
from bfcl.model_handler.base_handler import BaseHandler
from bfcl.model_handler.model_style import ModelStyle
from bfcl.model_handler.utils import ast_parse
import warnings


class GorillaHandler(BaseHandler):
    def __init__(self, model_name, temperature) -> None:
        super().__init__(model_name, temperature)
        self.model_style = ModelStyle.Gorilla
        self.is_fc_model = True
        self._usage_warning_shown = False

    def decode_ast(self, result, language="Python"):
        func = "[" + result + "]"
        decoded_output = ast_parse(func, language)
        return decoded_output

    def decode_execute(self, result):
        func = "[" + result + "]"
        decoded_output = ast_parse(func)
        execution_list = []
        for function_call in decoded_output:
            for key, value in function_call.items():
                execution_list.append(
                    f"{key}({','.join([f'{k}={repr(v)}' for k, v in value.items()])})"
                )
        return execution_list

    #### FC methods ####

    def _query_FC(self, inference_data: dict):
        inference_data["inference_input_log"] = {
            "message": inference_data["message"],
            "tools": inference_data["tools"],
        }
        requestData = {
            "model": self.model_name,
            "messages": inference_data["message"],
            "functions": inference_data["tools"],
            "temperature": self.temperature,
        }
        url = "https://luigi.millennium.berkeley.edu:443/v1/chat/completions"

        start_time = time.time()
        api_response = requests.post(
            url,
            headers={
                "Content-Type": "application/json",
                "Authorization": "EMPTY",  # Hosted for free with ❤️ from UC Berkeley
            },
            data=json.dumps(requestData),
        )
        end_time = time.time()

        return api_response.json(), end_time - start_time

    def _pre_query_processing_FC(self, inference_data: dict, test_entry: dict) -> dict:
        inference_data["message"] = []
        return inference_data

    def _compile_tools(self, inference_data: dict, test_entry: dict) -> dict:
        # Gorilla OpenFunctions does not require any pre-processing
        inference_data["tools"] = test_entry["function"]

        return inference_data

    def _parse_query_response_FC(self, api_response: any) -> dict:

        if "usage" in api_response:
            input_token = api_response["usage"]["prompt_tokens"]
            output_token = api_response["usage"]["completion_tokens"]
        else:
            if not self._usage_warning_shown:
                warnings.warn("Usage information not found in the response. Token counts will be zero.", UserWarning)
                self._usage_warning_shown = True
            input_token = 0
            output_token = 0

        return {
            "model_responses": api_response["choices"][0]["message"]["content"],
            "input_token": input_token,
            "output_token": output_token,
        }

    def add_first_turn_message_FC(
        self, inference_data: dict, first_turn_message: list[dict]
    ) -> dict:
        inference_data["message"].extend(first_turn_message)
        return inference_data

    def _add_next_turn_user_message_FC(
        self, inference_data: dict, user_message: list[dict]
    ) -> dict:
        inference_data["message"].extend(user_message)
        return inference_data

    def _add_assistant_message_FC(
        self, inference_data: dict, model_response_data: dict
    ) -> dict:
        inference_data["message"].append(
            {
                "role": "assistant",
                "content": model_response_data["model_responses"],
            }
        )
        return inference_data

    def _add_execution_results_FC(
        self, inference_data: dict, execution_results: list[str], model_response_data: dict
    ) -> dict:
        for execution_result in execution_results:
            tool_message = {
                "role": "tool",
                "content": execution_result,
            }
            inference_data["message"].append(tool_message)

        return inference_data
