import base64
import binascii
import json
from typing import Any, cast


def set_str(stream: str) -> str:
    """Encode a string to base64.

    Args:
        stream: The string to encode.

    Returns:
        Base64-encoded string, or empty string on failure.
    """
    try:
        return base64.b64encode(stream.encode("utf-8")).decode("utf-8")
    except (UnicodeError, TypeError, AttributeError):
        pass
    return ""


def get_str(stream: str) -> str:
    """Decode a base64-encoded string.

    Args:
        stream: The base64 string to decode.

    Returns:
        Decoded string, or empty string on failure.
    """
    try:
        return base64.b64decode(stream.encode("utf-8")).decode("utf-8")
    except (UnicodeError, binascii.Error, AttributeError):
        pass
    return ""


def get_dict(stream: str) -> dict[str, Any]:
    """Decode a JSON dictionary from a base64-encoded string.

    Args:
        stream: The base64 string containing JSON.

    Returns:
        Decoded dictionary, or empty dict on failure.
    """
    try:
        return cast(dict[str, Any], json.loads(get_str(stream)))
    except json.JSONDecodeError:
        pass
    return {}


def set_dict(stream: dict[str, Any]) -> str:
    """Encode a dictionary as a base64 string.

    Args:
        stream: The dictionary to encode.

    Returns:
        Base64-encoded string, or empty string on failure.
    """
    try:
        return set_str(json.dumps(stream))
    except (TypeError, ValueError):
        pass
    return ""
