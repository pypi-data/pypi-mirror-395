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
import os
import time

from bfcl.model_handler.base_handler import BaseHandler
from bfcl.model_handler.constant import GORILLA_TO_OPENAPI
from bfcl.model_handler.model_style import ModelStyle
from bfcl.model_handler.utils import (
    ast_parse,
    convert_to_function_call,
    convert_to_tool,
    format_execution_results_prompting,
    func_doc_language_specific_pre_processing,
    system_prompt_pre_processing_chat_model,
)
from mistralai import Mistral
import warnings


class MistralHandler(BaseHandler):
    def __init__(self, model_name, temperature) -> None:
        super().__init__(model_name, temperature)
        self.model_style = ModelStyle.Mistral
        self._usage_warning_shown = False

        self.client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))

    def decode_ast(self, result, language="Python"):
        if "FC" in self.model_name:
            decoded_output = []
            for invoked_function in result:
                name = list(invoked_function.keys())[0]
                params = json.loads(invoked_function[name])
                decoded_output.append({name: params})
            return decoded_output
        else:
            func = result
            func = func.replace("\\_", "_")
            if not func.startswith("["):
                func = "[" + func
            if not func.endswith("]"):
                func = func + "]"
            decoded_output = ast_parse(func, language)
            return decoded_output

    def decode_execute(self, result):
        if "FC" in self.model_name:
            function_call = convert_to_function_call(result)
            return function_call
        else:
            func = result
            func = func.replace("\\_", "_")
            decode_output = ast_parse(func)
            execution_list = []
            for function_call in decode_output:
                for key, value in function_call.items():
                    execution_list.append(
                        f"{key}({','.join([f'{k}={repr(v)}' for k, v in value.items()])})"
                    )
            return execution_list

    #### FC methods ####

    def _query_FC(self, inference_data: dict):
        message = inference_data["message"]
        tool = inference_data["tools"]
        inference_data["inference_input_log"] = {
            "message": message,
            "tools": tool,
        }

        start_time = time.time()
        api_response = self.client.chat.complete(
            model=self.model_name.replace("-FC", ""),
            messages=message,
            tools=tool,
            temperature=self.temperature,
        )
        end_time = time.time()

        return api_response, end_time - start_time

    def _pre_query_processing_FC(self, inference_data: dict, test_entry: dict) -> dict:
        inference_data["message"] = []
        return inference_data

    def _compile_tools(self, inference_data: dict, test_entry: dict) -> dict:
        functions: list = test_entry["function"]
        test_category: str = test_entry["id"].rsplit("_", 1)[0]

        functions = func_doc_language_specific_pre_processing(functions, test_category)
        tools = convert_to_tool(functions, GORILLA_TO_OPENAPI, self.model_style)

        inference_data["tools"] = tools

        return inference_data

    def _parse_query_response_FC(self, api_response: any) -> dict:
        try:
            model_responses = [
                {func_call.function.name: func_call.function.arguments}
                for func_call in api_response.choices[0].message.tool_calls
            ]
            tool_call_func_names = [
                func_call.function.name
                for func_call in api_response.choices[0].message.tool_calls
            ]
            tool_call_ids = [
                func_call.id for func_call in api_response.choices[0].message.tool_calls
            ]
        except:
            model_responses = api_response.choices[0].message.content
            tool_call_func_names = []
            tool_call_ids = []

        if "usage" in api_response.model_dump():
            input_token = api_response.usage.prompt_tokens
            output_token = api_response.usage.completion_tokens
        else:
            if not self._usage_warning_shown:
                warnings.warn("Usage information not found in the response. Token counts will be zero.", UserWarning)
                self._usage_warning_shown = True
            input_token = 0
            output_token = 0

        return {
            "model_responses": model_responses,
            "model_responses_message_for_chat_history": api_response.choices[0].message,
            "tool_call_func_names": tool_call_func_names,
            "tool_call_ids": tool_call_ids,
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
            model_response_data["model_responses_message_for_chat_history"]
        )
        return inference_data

    def _add_execution_results_FC(
        self, inference_data: dict, execution_results: list[str], model_response_data: dict
    ) -> dict:
        for execution_result, func_name, tool_call_id in zip(
            execution_results,
            model_response_data["tool_call_func_names"],
            model_response_data["tool_call_ids"],
        ):
            tool_message = {
                "role": "tool",
                "name": func_name,
                "content": execution_result,
                "tool_call_id": tool_call_id,
            }
            inference_data["message"].append(tool_message)
        return inference_data

    #### Prompting methods ####

    def _query_prompting(self, inference_data: dict):
        message = inference_data["message"]
        inference_data["inference_input_log"] = {"message": message}

        start_time = time.time()
        api_response = self.client.chat.complete(
            model=self.model_name,
            messages=message,
            temperature=self.temperature,
        )
        end_time = time.time()

        return api_response, end_time - start_time

    def _pre_query_processing_prompting(self, test_entry: dict) -> dict:
        functions: list = test_entry["function"]
        test_category: str = test_entry["id"].rsplit("_", 1)[0]

        functions = func_doc_language_specific_pre_processing(functions, test_category)

        test_entry["question"][0] = system_prompt_pre_processing_chat_model(
            test_entry["question"][0], functions, test_category
        )

        return {"message": []}

    def _parse_query_response_prompting(self, api_response: any) -> dict:
        if "usage" in api_response.model_dump():
            input_token = api_response.usage.prompt_tokens
            output_token = api_response.usage.completion_tokens
        else:
            if not self._usage_warning_shown:
                warnings.warn("Usage information not found in the response. Token counts will be zero.", UserWarning)
                self._usage_warning_shown = True
            input_token = 0
            output_token = 0

        return {
            "model_responses": api_response.choices[0].message.content,
            "model_responses_message_for_chat_history": api_response.choices[0].message,
            "input_token": input_token,
            "output_token": output_token,
        }

    def add_first_turn_message_prompting(
        self, inference_data: dict, first_turn_message: list[dict]
    ) -> dict:
        inference_data["message"].extend(first_turn_message)
        return inference_data

    def _add_next_turn_user_message_prompting(
        self, inference_data: dict, user_message: list[dict]
    ) -> dict:
        inference_data["message"].extend(user_message)
        return inference_data

    def _add_assistant_message_prompting(
        self, inference_data: dict, model_response_data: dict
    ) -> dict:
        inference_data["message"].append(
            model_response_data["model_responses_message_for_chat_history"]
        )
        return inference_data

    def _add_execution_results_prompting(
        self, inference_data: dict, execution_results: list[str], model_response_data: dict
    ) -> dict:
        formatted_results_message = format_execution_results_prompting(
            inference_data, execution_results, model_response_data
        )
        inference_data["message"].append(
            {"role": "user", "content": formatted_results_message}
        )

        return inference_data
