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

from bfcl.model_handler.local_inference.base_oss_handler import OSSHandler
from bfcl.model_handler.utils import convert_to_function_call
from overrides import override


class GlaiveHandler(OSSHandler):
    def __init__(self, model_name, temperature) -> None:
        super().__init__(model_name, temperature)

    @override
    def decode_ast(self, result, language="Python"):
        function_call = result.split("<functioncall>")[-1]
        function_call = function_call.replace("'", "")
        decoded_function = json.loads(function_call)
        for key, value in decoded_function["arguments"].items():
            if language == "Python":
                pass
            else:
                # all values of the json are casted to string for java and javascript
                decoded_function["arguments"][key] = str(
                    decoded_function["arguments"][key]
                )
        decoded_result = [{decoded_function["name"]: decoded_function["arguments"]}]
        return decoded_result

    @override
    def decode_execute(self, result):
        function_call = result.split("<functioncall>")[-1]
        function_call = function_call.replace("'", "")
        decoded_function = json.loads(function_call)
        decoded_result = [{decoded_function["name"]: decoded_function["arguments"]}]
        return convert_to_function_call(decoded_result)
