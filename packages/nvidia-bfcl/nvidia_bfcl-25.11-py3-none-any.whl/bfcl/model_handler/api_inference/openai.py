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
import requests

from bfcl.model_handler.base_handler import BaseHandler
from bfcl.model_handler.constant import GORILLA_TO_OPENAPI, UNDERSCORE_TO_DOT
from bfcl.model_handler.model_style import ModelStyle
from bfcl.model_handler.utils import (
    combine_consecutive_user_prompts,
    convert_system_prompt_into_user_prompt,
    convert_to_function_call,
    convert_to_tool,
    default_decode_ast_prompting,
    default_decode_execute_prompting,
    format_execution_results_prompting,
    func_doc_language_specific_pre_processing,
    system_prompt_pre_processing_chat_model,
)
from openai import OpenAI, RateLimitError
import warnings


class OpenAIHandler(BaseHandler):
    def __init__(self, model_name, base_url, temperature=0.0, native_calling=False) -> None:
        super().__init__(model_name, temperature)
        self.model_style = ModelStyle.OpenAI
        self.base_url = base_url
        self.is_fc_model= native_calling
        self._usage_warning_shown = False

        # if native calling is requested, we dynamically add this model to
        # the list of models that outputs function names with dots
        # replaced with underscores
        if self.is_fc_model:
            UNDERSCORE_TO_DOT.append(model_name.replace("_", "/"))

    def decode_ast(self, result, language="Python"):
        if "FC" in self.model_name or self.is_fc_model:
            decoded_output = []
            for invoked_function in result:
                name = list(invoked_function.keys())[0]
                params = json.loads(invoked_function[name])
                decoded_output.append({name: params})
            return decoded_output
        else:
            return default_decode_ast_prompting(result, language)

    def decode_execute(self, result):
        if "FC" in self.model_name or self.is_fc_model:
            return convert_to_function_call(result)
        else:
            return default_decode_execute_prompting(result)

    def generate_with_backoff(self, **kwargs):
        start_time = time.time()
        api_key = os.getenv("OPENAI_API_KEY")
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": self.model_name,
            **kwargs
        }

        api_response = requests.post(
        self.base_url,
        headers=headers,
        data=json.dumps(data)
        )
        api_response.raise_for_status()
        end_time = time.time()
        return json.loads(api_response.text), end_time - start_time

    #### FC methods ####

    def _query_FC(self, inference_data: dict):
        message: list[dict] = inference_data["message"]
        tools = inference_data["tools"]
        inference_data["inference_input_log"] = {"message": repr(message), "tools": tools}

        if len(tools) > 0:
            # o1 doesn't support temperature parameter
            # Beta limitation: https://platform.openai.com/docs/guides/reasoning/beta-limitations
            # Also, o1-mini does not support function calling
            if "o1" in self.model_name:
                return self.generate_with_backoff(
                    messages=message,
                    model=self.model_name.replace("-FC", ""),
                    tools=tools,
                )
            else:
                return self.generate_with_backoff(
                    messages=message,
                    model=self.model_name.replace("-FC", ""),
                    temperature=self.temperature,
                    tools=tools,
                )
        else:
            if "o1" in self.model_name:
                return self.generate_with_backoff(
                    messages=message,
                    model=self.model_name.replace("-FC", ""),
                )
            else:
                return self.generate_with_backoff(
                    messages=message,
                    model=self.model_name.replace("-FC", ""),
                    temperature=self.temperature,
                )

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
                {func_call['function']['name']: func_call['function']['arguments']}
                for func_call in api_response['choices'][0]['message']['tool_calls']
            ]
            tool_call_ids = [
                func_call['id'] for func_call in api_response['choices'][0]['message']['tool_calls']
            ]
        except Exception:
            print("Could not extract called tools. Using generated content instead.")
            model_responses = api_response['choices'][0]['message']['content']
            tool_call_ids = []

        print("model responses", model_responses)
        model_responses_message_for_chat_history = api_response['choices'][0]['message']
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
            "model_responses": model_responses,
            "model_responses_message_for_chat_history": model_responses_message_for_chat_history,
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
        self,
        inference_data: dict,
        execution_results: list[str],
        model_response_data: dict,
    ) -> dict:
        # Add the execution results to the current round result, one at a time
        for execution_result, tool_call_id in zip(
            execution_results, model_response_data["tool_call_ids"]
        ):
            tool_message = {
                "role": "tool",
                "content": execution_result,
                "tool_call_id": tool_call_id,
            }
            inference_data["message"].append(tool_message)

        return inference_data

    #### Prompting methods ####

    def _query_prompting(self, inference_data: dict):
        inference_data["inference_input_log"] = {"message": repr(inference_data["message"])}

        # o1 and o1-mini don't support temperature parameter
        # Beta limitation: https://platform.openai.com/docs/guides/reasoning/beta-limitations
        if "o1" in self.model_name:
            return self.generate_with_backoff(
                messages=inference_data["message"],
                model=self.model_name,
            )
        else:
            return self.generate_with_backoff(
                messages=inference_data["message"],
                model=self.model_name,
                temperature=self.temperature,
            )

    def _pre_query_processing_prompting(self, test_entry: dict) -> dict:
        functions: list = test_entry["function"]
        test_category: str = test_entry["id"].rsplit("_", 1)[0]

        functions = func_doc_language_specific_pre_processing(functions, test_category)

        test_entry["question"][0] = system_prompt_pre_processing_chat_model(
            test_entry["question"][0], functions, test_category
        )
        # Special handling for o1-mini as it doesn't support system prompts yet
        # o1 is fine with system prompts
        if "o1-mini" in self.model_name:
            for round_idx in range(len(test_entry["question"])):
                test_entry["question"][round_idx] = convert_system_prompt_into_user_prompt(
                    test_entry["question"][round_idx]
                )
                test_entry["question"][round_idx] = combine_consecutive_user_prompts(
                    test_entry["question"][round_idx]
                )

        return {"message": []}

    def _parse_query_response_prompting(self, api_response: any) -> dict:
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
            "model_responses": api_response['choices'][0]['message']['content'],
            "model_responses_message_for_chat_history": api_response['choices'][0]['message'],
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
