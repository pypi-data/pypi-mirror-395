import base64
import typing

import farmhash
from ._strings import encode_base32
from pydantic import BaseModel
import orjson

T = typing.TypeVar("T", bound=type)


def serialize_any(obj: typing.Any) -> str:
    if isinstance(obj, BaseModel):
        return obj.model_dump_json(exclude_none=True)
    elif isinstance(obj, (dict, list, tuple)):
        return orjson.dumps(
            obj, option=orjson.OPT_SORT_KEYS, default=serialize_any
        ).decode()
    elif isinstance(obj, (str, int, float)):
        return str(obj)
    else:
        raise ValueError(f"Cannot serialize {obj}")


def is_int(string) -> bool:
    try:
        int(string)
        return True
    except (ValueError, TypeError):
        return False


def to_int(v) -> typing.Optional[int]:
    try:
        return int(v)
    except (ValueError, TypeError):
        return None


def signed_64_to_unsigned_128(num: int) -> int:
    # Python automatically handles integer promotion to larger bit widths.
    # For a negative number, add 2^64 to shift its representation to the upper 64 bits of the 128-bit space.
    return num + (1 << 64) if num < 0 else num


def int_to_base62(num: int) -> str:
    # Characters to be used in base-62 encoding
    characters = (
        "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"  # # noqa: E501
    )

    if num == 0:
        return characters[0]

    num = signed_64_to_unsigned_128(num)

    base62 = []
    while num:
        num, remainder = divmod(num, 62)
        base62.append(characters[remainder])

    # The final string is built in reverse
    return "".join(reversed(base62))


def to_float(v) -> typing.Optional[float]:
    try:
        return float(v)
    except (ValueError, TypeError):
        return None


def to_numeric(v) -> typing.Optional[typing.Union[int, float]]:
    try:
        return int(v)
    except (ValueError, TypeError):
        try:
            return float(v)
        except ValueError:
            return None


def farmhash_string(s: str, to_base62: bool = False) -> str:
    hash_value = farmhash.hash64(s)
    hash_str = encode_base32(hash_value)
    if to_base62:
        return int_to_base62(hash_value)
    return hash_str


def farmhash_bytes(s: str) -> bytes:
    return farmhash.hash64(s).to_bytes(8, "big")


# def farmhash_any(obj: typing.Any, to_base62: bool = True):
#     if isinstance(obj, BaseModel):
#         _data = orjson.dumps(
#             obj.model_dump_json(exclude_none=True), option=orjson.OPT_SORT_KEYS
#         )
#         return farmhash_string(_data, to_base62=to_base62)
#     elif isinstance(obj, dict):
#         _data = orjson.dumps(
#             {k: farmhash_any(v) for k, v in obj.items() if v is not None},
#             option=orjson.OPT_SORT_KEYS,
#         )
#         return farmhash_string(_data, to_base62=to_base62)
#     elif isinstance(obj, list):
#         _data = orjson.dumps(sorted([farmhash_any(o) for o in obj]))
#         return farmhash_string(_data, to_base62=to_base62)
#     elif isinstance(obj, (str, int, float)):
#         return farmhash_string(str(obj), to_base62=to_base62)
#     else:
#         _data = orjson.dumps(obj, option=orjson.OPT_SORT_KEYS)
#         return farmhash_string(_data, to_base62=to_base62)


def farmhash_hex(s: str) -> str:
    return farmhash_bytes(s).hex()


def b64_decode(string: typing.Any) -> str:
    """Decode a base64 string"""

    if not isinstance(string, str):
        string = str(string)
    assert isinstance(string, str)

    # check if string is base64
    try:
        decoded = base64.b64decode(string)
        if base64.b64encode(decoded).decode("utf-8") == string:
            return decoded.decode("utf-8")
    except Exception:
        pass
    return string


def b64_encode(string: typing.Any) -> str:
    """Encode a string to base64"""

    if not isinstance(string, str):
        string = str(string)

    return base64.b64encode(string.encode("utf-8")).decode("utf-8")
