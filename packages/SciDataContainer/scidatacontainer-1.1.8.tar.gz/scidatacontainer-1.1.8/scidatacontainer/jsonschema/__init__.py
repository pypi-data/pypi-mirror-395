from __future__ import annotations  # required for |-operator in typing

__all__ = [
           "content",
           "meta",
           "validate",
           "VERSIONS_AVAILABLE",
           ]

import json
import os
from packaging import version

import jsonschema
from jsonschema.validators import Draft202012Validator, validator_for
from jsonschema.exceptions import ValidationError

_DIR = os.path.dirname(os.path.abspath(__file__))

content = {}
"""dict: Dictionary containing all available schemas for content.json
validation.

:meta hide-value:
"""

meta = {}
"""dict: Dictionary containing all available schemas for meta.json
validation.

:meta hide-value:
"""


def _translate_validation_error(exception: ValidationError,
                                filename: str):
    """Translate a jsonschema validation exception to a user friendly error
    message.

    This simply overwrites the `message` attribute of the exception.

    Args:
        exception: The exception thrown by the jsonschema library.
        filename: Filename where the problem was found.

    Raises:
        jsonschema.exceptions.ValidationError: Modified exception.
    """
    if "errorMessage" in exception.validator_value:
        exception.message = exception.validator_value["errorMessage"]
    elif exception.validator == "required":
        exception.message = exception.message + " in " + filename + ".json."
    elif exception.validator == "format":
        exception.message = "Value of '" + exception.path[0] + "' in " +\
                            filename + ".json has the wrong format: " +\
                            exception.message + "."
    elif exception.validator == "type":
        exception.message = "Value of '" + exception.path[0] + "' in " +\
                            filename + ".json has the wrong type: " +\
                            exception.message + "."
    elif exception.validator == "pattern":
        exception.message = "Value of '" + exception.path[0] + "' in " +\
                            filename + ".json has the wrong format: "
        if "patternErrorMessage" in exception.schema:
            exception.message += exception.schema["patternErrorMessage"]
        else:
            exception.message += exception.message + "."

    raise exception


def _guess_schema(instance: dict) -> (dict, str):
    """Guess the schema type and version from an instance.

    The schema is guessed by finding the schema which throws the lowest amount
    of errors during validation.

    Args:
        instance: Instance with unknown schema.

    Returns:
        schema: The schema that fits the best
        schema_name: schema type of the best match ('meta' or 'content')
    """
    schema = None
    schema_name = None
    min_errors = 1e30

    for key, s in content.items():
        cls = validator_for(s)
        num_errors = 0
        for _ in cls(s).iter_errors(instance):
            num_errors += 1
        if num_errors < min_errors:
            min_errors = num_errors
            schema = s
            schema_name = "content"

    for key, s in meta.items():
        cls = validator_for(s)
        num_errors = 0
        for _ in cls(s).iter_errors(instance):
            num_errors += 1
        if num_errors < min_errors:
            min_errors = num_errors
            schema = s
            schema_name = "meta"

    return schema, schema_name


def validate(instance: dict,
             schema: dict | None = None,
             schema_name: str | None = None,
             translate: bool = True,
             check_format: bool = True):
    """Validate if a dictionary fulfills the requirements of a
        SciDataContainer.

        If schema or schema_name is missing the values are guessed by finding
        the best overlap with one of the schemas.

        Args:
            instance: meta data dictionary.
            schema: schema used for validation.
            schema_name: "content" or "meta" used for more verbose error
                messages.
            translate: If true, replace the error message with more user
                friendly messages.
            check_format: If true, check the format of strings if they match
                the required format (e.g. date-time, email, ...).

        Raises:
            jsonschema.exceptions.ValidationError: Exception with details about
                the problem of the validated dictionary.
    """

    if check_format:
        format_checker = Draft202012Validator.FORMAT_CHECKER
    else:
        format_checker = None

    if (not schema) or (not schema_name) or\
            (schema_name not in ["meta", "content"]):
        schema, schema_name = _guess_schema(instance)

    try:
        jsonschema.validate(schema=schema,
                            instance=instance,
                            format_checker=format_checker)
    except ValidationError as e:
        if translate:
            _translate_validation_error(e, schema_name)
        else:
            raise


VERSIONS_AVAILABLE = []

for filename in os.listdir(_DIR):
    if filename.startswith("SciDataContainer.content."):
        modelVersion = filename[len("SciDataContainer.content."):]
        modelVersion = modelVersion[:-len(".schema.json")]
        if modelVersion not in VERSIONS_AVAILABLE:
            VERSIONS_AVAILABLE.append(modelVersion)
        with open(_DIR + "/" + filename, 'r') as content_file:
            content_json = content_file.read()
            content[modelVersion] = json.loads(content_json)
            Draft202012Validator.check_schema(content[modelVersion])

    elif filename.startswith("SciDataContainer.meta."):
        modelVersion = filename[len("SciDataContainer.meta."):]
        modelVersion = modelVersion[:-len(".schema.json")]
        if modelVersion not in VERSIONS_AVAILABLE:
            VERSIONS_AVAILABLE.append(modelVersion)
        with open(_DIR + "/" + filename, 'r') as meta_file:
            meta_json = meta_file.read()
            meta[modelVersion] = json.loads(meta_json)
            Draft202012Validator.check_schema(meta[modelVersion])

VERSIONS_AVAILABLE.sort(key=version.parse)
