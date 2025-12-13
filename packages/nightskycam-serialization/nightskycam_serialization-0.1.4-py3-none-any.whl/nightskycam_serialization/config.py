from typing import Any, Dict, Optional, Tuple

from .fix import deserialize_fix_dict, serialize_fix_dict
from .serialize import ImproperMessage, deserialize, serialize

_None = "__None__"


def serialize_config_update(
    runner_name: str, config: Dict[str, Any], token: Optional[str] = None
) -> str:
    """
    For server to request runners of remote system to reconfigure
    themselves.

    Counterpart: [deserialize_config_update]()

    Arguments
      runner_name: name of the runner that needs reconfiguring
      config: the new configuration to apply.
      token: see [serialize.serialize]()

    Returns
      corresponding serialized message
    """

    d = {"runner_name": runner_name, "config": serialize_fix_dict(config)}
    return serialize(d, token=token)


def _deserialize_fix(value: Any) -> Any:
    # Casting back "__None__" to None.
    if isinstance(value, str) and value == "__None__":
        return None
    return value


def _deserialize_fix_config(config: Dict[str, Any]) -> Dict[str, Any]:
    return {k: _deserialize_fix(v) for k, v in config.items()}


def deserialize_config_update(
    message: str, token: Optional[str] = None
) -> Tuple[str, Dict[str, Any]]:
    """
    For system receiving configuration update request for a runner.

    Counterpart: [serialize_config_update]()

    Arguments
      message: the serialized request
      token: see [serialize.deserialize]()

    Returns
      Tuple:
      - the name of the runner that should update
      - the configuration
    """

    data = deserialize(message, required_keys=("runner_name", "config"), token=token)
    if not isinstance(data["config"], dict):
        raise ImproperMessage(
            f"configuration expected to be a dictionary, but got {data['config']} of type {type(data['config'])} instead."
        )
    return (str(data["runner_name"]), deserialize_fix_dict(data["config"]))
