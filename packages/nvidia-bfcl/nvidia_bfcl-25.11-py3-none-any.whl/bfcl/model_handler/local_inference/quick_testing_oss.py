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

from bfcl.model_handler.local_inference.base_oss_handler import OSSHandler
from overrides import override

"""
Note: 
This handler only have the `_format_prompt` method overridden to apply the chat template automatically. Other methods are inherited from the OSSHandler.
We DO NOT recommend using this handler directly. This handler only serve as a fallback, or for quick testing.
Formatting the prompt manually give us better control over the final formatted prompt and is generally recommended for advanced use cases.
"""


class QuickTestingOSSHandler(OSSHandler):
    def __init__(self, model_name, temperature) -> None:
        super().__init__(model_name, temperature)

    @override
    def _format_prompt(self, messages, function):

        formatted_prompt = self.tokenizer.apply_chat_template(
            messages, add_generation_prompt=True, tokenize=False
        )

        return formatted_prompt
