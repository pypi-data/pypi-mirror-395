"""This module provides utilities for unwrapping data after import."""

from __future__ import annotations

from typing import Any

from extended_data_types.json_utils import decode_json
from extended_data_types.toml_utils import decode_toml
from extended_data_types.yaml_utils import decode_yaml


def unwrap_raw_data_from_import(wrapped_data: str, encoding: str = "yaml") -> Any:
    """Unwraps the data that was wrapped for import.

    Args:
        wrapped_data (str): The wrapped data.
        encoding (str): The encoding format (default is 'yaml').

    Returns:
        Any: The unwrapped data.

    Raises:
        ValueError: If the encoding format is unsupported.
    """
    encoding_lower = encoding.casefold()
    if encoding_lower == "yaml":
        return decode_yaml(wrapped_data)
    if encoding_lower == "json":
        return decode_json(wrapped_data)
    if encoding_lower == "toml":
        return decode_toml(wrapped_data)

    error_message = f"Unsupported encoding format: {encoding}"
    raise ValueError(error_message)
