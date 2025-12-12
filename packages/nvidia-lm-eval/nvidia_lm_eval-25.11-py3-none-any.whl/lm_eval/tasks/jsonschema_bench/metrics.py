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

# Original Copyright EleutherAI.
# For the original license and copyright information, see the LICENSE file in this repository.

import ipaddress
import json
import logging
import uuid
from typing import Any, Dict


# check if jsonschema is installed
try:
    import jsonschema
    from jsonschema import Draft202012Validator, FormatChecker, ValidationError
except ImportError as e:
    raise ImportError(
        "jsonschema is not installed. Please install it using 'pip install jsonschema[format]'"
    ) from e

eval_logger = logging.getLogger(__name__)


def is_json_schema_valid(schema: dict):
    """
    Check if a JSON schema is valid.

    :param schema: A JSON schema.
    :return: True if the schema is valid, False otherwise.
    """
    try:
        # Check if the schema is valid
        jsonschema.Draft202012Validator.check_schema(schema)
        return True
    except jsonschema.SchemaError:
        return False


# Initialize the FormatChecker
format_checker = FormatChecker()


# Add custom format checkers
@format_checker.checks("ipv4")
def ipv4_check(value):
    ipaddress.IPv4Address(value)


@format_checker.checks("ipv6")
def ipv6_check(value):
    ipaddress.IPv6Address(value)


@format_checker.checks("uuid")
def uuid_check(value):
    uuid.UUID(value)


def schema_conform_with_format_checker(
    instance: Dict[str, Any], schema: Dict[str, Any]
) -> bool:
    """
    Validate a JSON instance against a schema with enhanced format checking.

    :param schema: The JSON schema to validate against.
    :param instance: The JSON instance to validate.
    :raises ValidationError: If the validation fails.
    """
    # first check if the schema is valid
    if not is_json_schema_valid(schema):
        raise ValidationError("The JSON schema is invalid.")
    validator = Draft202012Validator(schema, format_checker=format_checker)
    try:
        validator.validate(instance)
    except ValidationError as e:
        raise ValidationError(e.message)
    return True


def schema_compliance(references: list[str], predictions: list[str]) -> bool:
    assert len(references) == 1, (
        "We only have one reference for this task, which is the JSON schema."
    )
    assert len(predictions) == 1, (
        "Currently, we don't support pass@k for JSON schema validation."
    )
    reference = references[0]
    prediction = predictions[0]  # Since predictions is a list of lists

    json_schema = json.loads(reference.strip())
    try:
        json_obj = json.loads(prediction.strip().strip("```").strip("json"))
    except json.JSONDecodeError:
        return False

    try:
        schema_conform = schema_conform_with_format_checker(json_obj, json_schema)
    except Exception as e:
        eval_logger.error(f"Error: {e}")
        return False

    return schema_conform


def json_validity(references: list[str], predictions: list[str]) -> bool:
    assert len(predictions) == 1, (
        "Currently, we don't support pass@k for JSON schema validation."
    )
    prediction = predictions[0]  # Since predictions is a list of lists
    try:
        json.loads(prediction.strip().strip("```").strip("json").strip())
    except json.JSONDecodeError:
        return False
    return True
