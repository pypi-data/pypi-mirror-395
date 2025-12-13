from typing import Any, Dict, Iterable, Optional

import tomli
import tomli_w


class ImproperMessage(Exception):
    ...


class IncorrectToken(Exception):
    ...


_token_key: str = "__token__"


def _check_keys(required_keys: Iterable[str], d: Dict[str, Any]) -> None:
    """
    Raises an [improper_message.ImproperMessage]() error if any
    key is missing from d.
    """

    missing_keys = [rk for rk in required_keys if rk not in d.keys()]
    if missing_keys:
        raise ImproperMessage(f"missing key(s): {', '.join(missing_keys)}")


def serialize(d: Dict[str, Any], token: Optional[str] = None) -> str:
    """
    Cast d to a string.
    Counterpart: [deserialize]()

    If 'token' is not None, its value will be added to the dictionary
    under the key '__token__'. If this key already exists in d, a
    ValueError will be raised.
    """
    if token:
        if _token_key in d:
            raise ValueError(
                f"Can not serialize a dictionary with key '{_token_key}'"
                "(key reserved by nightskycam-serialization)"
            )
        d[_token_key] = token
    return tomli_w.dumps(d)


def deserialize(
    message: str,
    required_keys: Iterable = tuple(),
    token: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Cast message to a dictionary.
    Counterpart: [serialize]().

    Arguments
      message: the message to deserialize
      required_keys: if any of the keys is missing from the deserialized dictionary,
        an ImproperMessage error is raised
      token: if not None, the deserialized dictionary is expected to have a '__token__'
        key associated with this value. If not, an IncorrectToken error is raised.
    """
    data = tomli.loads(message)
    if token:
        if _token_key not in data:
            raise IncorrectToken(
                f"The key {_token_key} was expected in the message, but is missing"
            )
        if data[_token_key] != token:
            raise IncorrectToken(
                "Received message contains the token "
                f"{data[_token_key]}, "
                f"which does not match the specified token {token}."
            )
        del data[_token_key]
    if required_keys:
        _check_keys(required_keys, data)
    return data
