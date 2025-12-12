from typing import Any, Tuple, Dict
import hashlib
import base64
import hmac


def if_null_get(value: Any, default: Any) -> Any:
    """
    Evaluate the given value, if is None return default argument
    otherwise given value
    """
    return default if value is None else value


def get_hmac(key: str, msg: str) -> str:
    """Hash message authentication code generator

    Args:
        key (str): [The starting key for the hash]
        msg (str): [Initial input for the hash, or None.]

    Returns:
        str: [Hash]
    """
    hash_value: bytes = hmac.new(
        str(key).encode("utf-8"), msg=str(msg).encode("utf-8"), digestmod=hashlib.sha256
    ).digest()
    return base64.b64encode(hash_value).decode()


def get_hash(value: str, charset: str = "utf-8") -> str:
    """Hash Generator

    Args:
        value (str): value

    Returns:
        str: sha256 hash
        @param value:
        @param charset:
    """
    return hashlib.sha256(value.encode(charset)).hexdigest()


def is_built_type(value: Any) -> bool:
    """Check if type of value provides is built in Python

    Args:
        value (Any): value

    Returns:
        [bool]: true if type of value is built in Python
    """
    return type(value) in (
        bytearray,
        str,
        list,
        tuple,
        range,
        dict,
        int,
        complex,
        set,
        bytes,
        bool,
        float,
    )


def unpack(values: Dict) -> Tuple:
    """
    Unpack dictionary values
    @param values:
    @return: tuple of dict values
    """
    return tuple([values[k] for k in values.keys()])
