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
import sys
from pathlib import Path
from bfcl.constant import VERSION_PREFIX
from bfcl.utils import parse_test_category_argument
from .custom_data_model import (
    OpenAIFormatData,
    NativeFormatQuestionData,
    NativeFormatGroundTruthData,
)
from typing import Dict, List, Union
from jinja2.sandbox import SandboxedEnvironment


import logging

logger = logging.getLogger(__name__)


env = SandboxedEnvironment()


def render_template(
    template: Union[str, Dict, List], context: Dict
) -> Union[str, Dict, List]:
    """
    Render the provided template.

    Support string, lists and dictionary templates.
    Only strings are interpreted as templates and rendered.

    Args:
        template: The template.
        context: Context variables to be used when rendering.

    Returns:
        (Union[str, Dict] The rendered template.
    """
    # For a dictionary, we go recursively
    if isinstance(template, dict):
        return {k: render_template(v, context) for k, v in template.items()}
    # For a list as well
    elif isinstance(template, list):
        return [render_template(v, context) for v in template]
    # For a string we render
    elif isinstance(template, str):
        rendered_str = env.from_string(template).render(context)
        if "tojson" in template:
            # Decode string into json if it's expected
            rendered = json.loads(rendered_str)
        else:
            rendered = rendered_str
        return rendered
    # Anything else stays the same
    else:
        return template


def convert_json_object_to_question(item: Dict, question_id: str):
    """
    Convert the item to the question object in native format

    Args:
        item: The item
        question_id: The question id
    Returns:
        The native object
    """
    # Create new object with required changes for main output
    native_obj = {
        "id": question_id,  # Add incremental ID
        "question": item["messages"],  # Rename messages to question
        "function": [],  # Initialize the function list
    }

    # Handle tools to function conversion
    for tool in item["tools"]:
        if tool["type"] == "function":
            native_obj["function"].append(tool["function"])
    return native_obj


def convert_json_object_to_ground_truth(item: Dict, question_id: str):
    """
    Convert the item to the ground truth object in native format

    Args:
        item: The item
        question_id: The question id
    Returns:
        The ground truth object
    """
    # Create and write ground truth object if available

    gt_obj = {"id": question_id, "ground_truth": item["tool_calls_ground_truth"]}
    return gt_obj


def convert_json_file_format(
    test_category: str,
    input_file: str,
    output_file: str,
    ground_truth_file: str,
    data_template: Dict = None,
):
    """
    Converts data.json to two output files:

    1. output_file: with the following changes:
       - Add an 'id' field with incremental numbers
       - Rename 'messages' to 'question'
       - Move tools[i]["function"] to 'function' field as an array

    2. ground_truth_file: containing ground truth data:
       - Add an 'id' field with incremental numbers
       - Add a 'ground_truth' field with the value of 'tool_calls_ground_truth'

    Output is written as JSON Lines format (one JSON object per line)

    Args:
        input_file (str): Path to the input JSON file
        output_file (str): Path to the output JSON file
        ground_truth_file (str): Path to the ground truth output file
    """
    failure_details = []
    try:
        with open(input_file, "r") as infile, open(output_file, "w") as outfile, open(
            ground_truth_file, "w"
        ) as gt_file:

            for i, line in enumerate(infile):
                try:
                    # Parse the JSON object from the current line
                    item = json.loads(line.strip())
                    if data_template:
                        item = render_template(
                            data_template, context={**item, "item": item}
                        )
                    # validate item
                    OpenAIFormatData(**item)
                    question_id = f"{test_category}_{i}"
                    # convert item to question
                    question = convert_json_object_to_question(item, question_id)
                    # convert item to ground truth
                    ground_truth = convert_json_object_to_ground_truth(
                        item, question_id
                    )

                    # Write the converted object as a single line in the output file
                    outfile.write(json.dumps(question) + "\n")
                    gt_file.write(json.dumps(ground_truth) + "\n")

                except Exception as e:
                    failure_details.append(
                        {
                            "line": i + 1,
                            "error": f"Dataset conversion error: {e}",
                            "data": line,
                        }
                    )
                    logger.error(f"Dataset conversion error: {e}")
        logger.info(
            f"Conversion completed. Output written to {output_file} and {ground_truth_file}"
        )

    except FileNotFoundError as e:
        failure_details.append({"error": f"File not found: {e}"})
        logger.error(f"File not found: {e}")
    except Exception as e:
        failure_details.append({"error": f"An error occurred: {e}"})
        logger.error(f"An error occurred: {e}")

    return failure_details


def convert_openai_format_to_native(
    test_category: str,
    input_file: str,
    output_dir: str,
    results_dir: str,
    data_template: Dict = None,
):
    """
    Converts OpenAI format to native format

    Args:
        test_category: The test category
        input_file: The input file path for openai format data
        output_dir: The output directory for storing temporary native format files
        results_dir: The results directory for storing failure details
        data_template: The data template
    """
    # create dir if not exists
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    ground_truth_dir = os.path.join(output_dir, "possible_answer")
    Path(ground_truth_dir).mkdir(parents=True, exist_ok=True)
    # convert openai format to native format
    file_name = f"{VERSION_PREFIX}_{test_category}.json"
    output_file = os.path.join(output_dir, file_name)
    ground_truth_file = os.path.join(ground_truth_dir, file_name)
    failure_details = convert_json_file_format(
        test_category, input_file, output_file, ground_truth_file, data_template
    )
    Path(results_dir).mkdir(parents=True, exist_ok=True)
    if failure_details:
        # save failure details to a file
        failure_details_file = os.path.join(
            results_dir, "validation_failure_details.json"
        )
        # dump a list of failure details to a file
        with open(failure_details_file, "w") as f:
            json.dump(failure_details, f)
        logger.error(
            f"Conversion failed with the details saved in {failure_details_file}"
        )
        sys.exit(1)
    else:
        logger.info(
            f"Conversion completed. Output written to {output_file} and {ground_truth_file}"
        )


def validate_native_format_file(question_file: str, ground_truth_file: str):
    """
    Validate the native format file including both question question and ground truth question

    Args:
        question_file: The question file path
        ground_truth_file: The ground truth file path
        output_dir: Optional output directory for failure details
    """
    failure_details = validate_native_format_data_model(
        question_file, NativeFormatQuestionData
    )
    failure_details.extend(
        validate_native_format_data_model(
            ground_truth_file, NativeFormatGroundTruthData
        )
    )
    return failure_details


def validate_native_format_data_model(file: str, data_model: NativeFormatQuestionData):
    """
    Validate the native format file with the given data model

    Args:
        file: The question file path
        data_model: The data model
    """
    failure_details = []
    # check if the file exists
    if not os.path.exists(file):
        failure_details.append({"error": f"File not found: {file}"})
        logger.error(f"File not found: {file}")
        return failure_details
    # read the file
    with open(file, "r") as infile:
        for i, line in enumerate(infile):
            try:
                data_model(**json.loads(line))
            except Exception as e:
                failure_details.append(
                    {
                        "line": i + 1,
                        "error": f"Validation failed for line {i+1}: {e}",
                        "data": line,
                    }
                )
                logger.error(f"Validation failed for question {i+1}: {e}")
    return failure_details


def get_test_category_list(test_category: str):
    """
    Get the test category list from the input string
    Args:
        test_category: The test category
    Returns:
        The test category list
    """
    if "," in test_category:
        test_category_list = test_category.split(",")
    else:
        test_category_list = [test_category]
    _, all_test_categories = parse_test_category_argument(test_category_list)
    return all_test_categories


def validate_native_format_dataset(data_dir: str, test_category: str, output_dir: str):
    """
    Validate the native format dataset for all the test categories

    Args:
        data_dir: The data directory
        test_category: The test category
        output_dir: The output directory
    """
    test_category_list = get_test_category_list(test_category)
    for one_test_category in test_category_list:
        validate_one_native_format_dataset(data_dir, one_test_category, output_dir)


def validate_one_native_format_dataset(
    data_dir: str, test_category: str, output_dir: str
):
    """
    Validate the native format dataset for the individual test category

    Args:
        data_dir: The data directory
        test_category: The individual test category
        output_dir: The output directory
    """
    # skip multi-turn and relevance test category
    if "multi_turn" in test_category or "relevance" in test_category:
        logger.info(f"Skipping validation for test category: {test_category}")
        return

    question_file = os.path.join(data_dir, f"{VERSION_PREFIX}_{test_category}.json")
    ground_truth_file = os.path.join(
        data_dir, f"possible_answer/{VERSION_PREFIX}_{test_category}.json"
    )
    failure_details = validate_native_format_file(question_file, ground_truth_file)
    if failure_details:
        # save failure details to a file
        failure_details_file = os.path.join(
            output_dir, "validation_failure_details.json"
        )
        # dump a list of failure details to a file
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        with open(failure_details_file, "w") as f:
            json.dump(failure_details, f)
        logger.error(
            f"Validation failed with the details saved in {failure_details_file}"
        )
    else:
        logger.info(f"Validation passed for {question_file} and {ground_truth_file}")
