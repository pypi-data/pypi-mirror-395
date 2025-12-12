import json
import sys
from typing import Optional, Any
from pydantic import BeforeValidator
from typing_extensions import Annotated


def preprocess_json_string_to_list(data: Any) -> Optional[list[str]]:
    """
    Fix for MCP XML parameter serialization issue:
    When lists are passed through the MCP function calling interface's XML parameters,
    they are serialized as JSON strings (e.g., '["id1", "id2"]') rather than actual
    Python lists. This causes Pydantic validation to fail with "Input should be a valid list"
    errors. We parse the JSON string back to a list if needed to handle both direct Python
    calls (which pass actual lists) and MCP calls (which pass JSON strings).

    This validator runs BEFORE Pydantic's type validation.
    """
    sys.stderr.write(f"Preprocessing data: {data} (type: {type(data)})\n")

    if data is None:
        return None

    if isinstance(data, list):
        return data

    if isinstance(data, str):
        try:
            parsed = json.loads(data)
            sys.stderr.write(f"*** Parsed to: {parsed} (type: {type(parsed)})\n")
            return parsed
        except json.JSONDecodeError:
            sys.stderr.write(f"*** JSON decode failed, returning None\n")
            return None

    return data


# Custom type annotation for variable_ids that auto-parses JSON strings
JsonStringList = Annotated[Optional[list[str]], BeforeValidator(preprocess_json_string_to_list)]

