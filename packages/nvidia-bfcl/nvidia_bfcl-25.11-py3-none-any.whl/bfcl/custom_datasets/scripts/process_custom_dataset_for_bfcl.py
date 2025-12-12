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

import argparse
import json
import os
import sys
import tempfile
import logging
from pathlib import Path

from bfcl.custom_datasets.utils.process_custom_data import (
    convert_openai_format_to_native,
    validate_native_format_dataset,
)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    parser = argparse.ArgumentParser(description="Process custom datasets for BFCL evaluation.")
    parser.add_argument("--dataset_format", type=str, choices=["native", "openai"], required=True,
                        help="Format of the custom dataset.")
    parser.add_argument("--dataset_path", type=str, required=True,
                        help="Path to the custom dataset file (for openai) or directory (for native).")
    parser.add_argument("--test_category", type=str, required=True,
                        help="The test category for the dataset (e.g., simple, exec_simple).")
    parser.add_argument("--processing_output_dir", type=str, required=True,
                        help="Directory for storing conversion failure details or validation reports. "
                             "For openai format, a sub-temp directory for converted files will be created here or in /tmp.")
    parser.add_argument("--data_template_path", type=str, default=None,
                        help="Optional path to a JSON file defining the data template (for openai format).")

    args = parser.parse_args()

    data_template = None
    if args.data_template_path:
        try:
            with open(args.data_template_path, 'r') as f_template:
                data_template = json.load(f_template)
        except FileNotFoundError:
            logger.error(f"Data template file not found: {args.data_template_path}")
            sys.exit(1)
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding data template file {args.data_template_path}: {e}")
            sys.exit(1)

    bfcl_data_dir_to_export = None
    Path(args.processing_output_dir).mkdir(parents=True, exist_ok=True)

    if args.dataset_format == "native":
        logger.info(f"Validating native dataset at: {args.dataset_path}")
        validate_native_format_dataset(
            data_dir=args.dataset_path,
            test_category=args.test_category,
            output_dir=args.processing_output_dir  # For validation failure details
        )
        bfcl_data_dir_to_export = os.path.abspath(args.dataset_path)
        logger.info(f"Native dataset validated. BFCL_DATA_DIR should be: {bfcl_data_dir_to_export}")

    elif args.dataset_format == "openai":
        # Create a unique temporary directory for the converted native files
        # This directory will become the BFCL_DATA_DIR
        temp_conversion_dir = tempfile.mkdtemp(dir=args.processing_output_dir, prefix="bfcl_converted_native_")
        logger.info(f"Converting OpenAI dataset: {args.dataset_path}")
        logger.info(f"Converted native files will be stored in: {temp_conversion_dir}")
        logger.info(f"Failure details will be in: {args.processing_output_dir}")
        
        convert_openai_format_to_native(
            test_category=args.test_category,
            input_file=args.dataset_path,
            output_dir=temp_conversion_dir,    # This is where native files are written
            results_dir=args.processing_output_dir, # For conversion failure details
            data_template=data_template,
        )
        bfcl_data_dir_to_export = os.path.abspath(temp_conversion_dir)
        logger.info(f"OpenAI dataset converted. BFCL_DATA_DIR should be: {bfcl_data_dir_to_export}")

    else:
        # Should be caught by argparse choices, but as a safeguard:
        logger.error(f"Unsupported dataset format: {args.dataset_format}")
        sys.exit(1)

    # Print the path to be used for BFCL_DATA_DIR to stdout
    # This can be captured by the calling process
    if bfcl_data_dir_to_export:
        print(bfcl_data_dir_to_export)
    else:
        logger.error("Failed to determine BFCL_DATA_DIR path.")
        sys.exit(1)

if __name__ == "__main__":
    main()
