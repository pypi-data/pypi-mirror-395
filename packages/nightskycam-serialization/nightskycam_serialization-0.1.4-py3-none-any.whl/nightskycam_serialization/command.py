from dataclasses import asdict, dataclass
from typing import Dict, Optional, Tuple, Union

from .serialize import ImproperMessage, deserialize, serialize


def serialize_command(
    command_id: int, command: str, token: Optional[str] = None
) -> str:
    """
    Serialize a command to be executed on the system

    Counterpart, see: [deserialize_command]().

    Arguments
      command_id: unique identifier of the command
      command: the command to execute
      token: see [serialize.serialize]()

    Returns
      The serialized message
    """
    d: Dict[str, Union[int, str]] = {
        "command_id": command_id,
        "command": command,
    }
    return serialize(d, token=token)


def deserialize_command(message: str, token: Optional[str] = None) -> Tuple[int, str]:
    """
    Deserialize a message sent by the server into a command to
    be executed by the system.

    Counterpart, see [serialize_command]()

    Arguments
      message: the serialized message
      token: see [serialize.deserialize]()

    Returns
      command_id: unique identifier of the command
      command: the command to execute


    Raises
      [improper_message.ImproperMessage]() if message is not properly
      formated.
    """

    data = deserialize(
        message,
        required_keys=("command_id", "command"),
        token=token,
    )
    try:
        command_id = int(data["command_id"])
    except ValueError:
        raise ImproperMessage(
            "value for key 'command_id' should be an int, "
            f"but received value {data['command_id']} of type {type(data['command_id'])} instead."
        )

    return command_id, str(data["command"])


@dataclass
class CommandResult:
    """
    Summary of the "output" of a command executed on the system.
    """

    command_id: int
    command: str
    stdout: str = ""
    stderr: str = ""
    exit_code: str = ""
    error: str = ""


def serialize_command_result(result: CommandResult, token: Optional[str] = None) -> str:
    """
    Serialize a command output to a string.

    Counterpart method: [deserialize_command_result]().

    Arguments
      result: output of the command
      token: see [serialize.serialize]()

    Returns
      serialized result
    """
    data = asdict(result)
    return serialize(data, token=token)


def deserialize_command_result(
    message: str, token: Optional[str] = None
) -> CommandResult:
    """
    Deserialize a message into an instance of CommandResult

    Counterpart method: [serialize_command_result]().

    Arguments:
      message: the serialized message
      token: see [serialize.deserialize]()

    Returns
      The corresponding instance of CommandResult

    Raises
      [improper_message.ImproperMessage]() if message is not properly formatted.
    """

    data = deserialize(message, required_keys=tuple(), token=token)
    try:
        return CommandResult(**data)
    except TypeError as te:
        raise ImproperMessage(
            "failed to deserialize the message into an instance "
            f"of CommandResult: {te}"
        )
