from pathlib import Path
from typing import Any, Dict, TypeVar

from nightskyrunner.status import StatusDict

_None = "__None__"


SerialDict = TypeVar("SerialDict", Dict[str, Any], StatusDict)


def serialize_fix(value: Any) -> Any:
    """
    Sometimes python dictionary can not be serialized into
    toml. Here fixing the commonly encountered issue:

    - pathlib.Path (cast to string)
    - None (cast to the string "__None__")

    See: [deserialize_fix]()
    """

    if value is None:
        return _None
    if isinstance(value, Path):
        return str(value)
    return value


def serialize_fix_dict(config: SerialDict) -> SerialDict:
    """
    Applying [serialize_fix] to all values of the dictionary

    See: [deserialize_fix_dict]()
    """
    instance = type(config)()
    for k, v in config.items():
        instance[k] = serialize_fix(v)  # type: ignore
    return instance


def deserialize_fix(value: Any) -> Any:
    """
    Casting the string "__None__" to None.

    See: [serialize_fix]()
    """

    # Casting back "__None__" to None.
    if isinstance(value, str) and value == "__None__":
        return None
    return value


def deserialize_fix_dict(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Applying [deserialize_fix]() to all values of the dictionary.

    See: [serialize_fix_dict]().
    """

    return {k: deserialize_fix(v) for k, v in config.items()}
