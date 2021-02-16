from json import loads as jloads
from json import dumps as jdumps
from base64 import b64decode, b64encode


def set_str(stream: str) -> str:
    try:
        return b64encode(stream.encode("utf8")).decode("utf-8")
    except Exception:
        pass
    return ""


def get_str(stream: str) -> str:
    try:
        return b64decode(stream.encode("utf8")).decode("utf-8")
    except Exception:
        pass
    return ""


def get_dict(stream: str) -> dict:
    try:
        return jloads(get_str(stream))
    except Exception:
        pass
    return {}


def set_dict(stream: dict) -> str:
    try:
        return set_str(jdumps(stream))
    except Exception:
        pass
    return ""
