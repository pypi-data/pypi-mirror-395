import base64
import datetime
import re
import typing

import orjson

from ._dates import parse_timestamp
from ._regex import (
    RE_DOMAIN_NAMES,
    RE_EMAIL,
    RE_HTML,
    RE_JAVASCRIPT,
    RE_PHONE_NUMBER,
    RE_UUID,
    REGEX_CAMEL_CASE,
)


def is_uuid(s: str) -> bool:
    return (
        re.match(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", s)
        is not None
    )


def camel_to_slug(s: str, force_lower: bool = True) -> str:
    # Step 1: Handle acronyms and numbers, keeping numbers joined with preceding letters
    s = REGEX_CAMEL_CASE.sub(r"-", s)

    # Step 2: Remove any leading dash
    s = s.lstrip("-")

    # Step 3: Convert to lowercase and replace multiple dashes with single ones
    return re.sub(r"-+", "-", s.lower() if force_lower else s)


def camel_to_snake(name: str) -> str:
    # First, handle consecutive uppercase letters followed by lowercase
    # e.g., "HTTPSConnection" -> "HTTPS_Connection"
    name = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", name)
    # Then handle normal camelCase transitions
    # e.g., "myVariable" -> "my_Variable"
    name = re.sub(r"([a-z])([A-Z])", r"\1_\2", name)
    return name.lower()


def camel_to_kebab(name: str, protected_acronyms: list[str] | None = None) -> str:
    if protected_acronyms:
        # Sort acronyms by length (descending) to handle longer matches first
        sorted_acronyms = sorted(protected_acronyms, key=len, reverse=True)
        result = ""
        remaining = name

        while remaining:
            matched = False
            for acronym in sorted_acronyms:
                if remaining.startswith(acronym):
                    # Add separator if this isn't the first part
                    if result:
                        result += "-"
                    result += acronym
                    remaining = remaining[len(acronym) :]
                    matched = True
                    break

            if not matched:
                # Find the next capital letter or end of string
                match = re.search(r"[A-Z]", remaining[1:])
                if match:
                    # Extract this word
                    next_cap_index = match.start() + 1
                    word = remaining[:next_cap_index]
                    remaining = remaining[next_cap_index:]
                else:
                    # Rest of the string
                    word = remaining
                    remaining = ""

                # Add separator if this isn't the first part
                if result:
                    result += "-"
                result += word.lower()

        return result
    else:
        # First, handle consecutive uppercase letters followed by lowercase
        name = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1-\2", name)
        # Then handle normal camelCase transitions
        name = re.sub(r"([a-z])([A-Z])", r"\1-\2", name)
        return name.lower()


def snake_to_camel(name: str) -> str:
    words = name.split("_")
    # First word is lowercase, rest are title case
    return words[0].lower() + "".join(word.title() for word in words[1:])


def snake_to_kebab(name: str) -> str:
    return name.replace("_", "-")


def kebab_to_camel(name: str) -> str:
    words = name.split("-")
    # First word is lowercase, rest are title case
    return words[0].lower() + "".join(word.title() for word in words[1:])


def kebab_to_snake(name: str) -> str:
    return name.replace("-", "_")


def slug_to_camel(s: str) -> str:
    words = s.split("-")
    # First word is lowercase, rest are title case
    return words[0].lower() + "".join(word.title() for word in words[1:])


def slug_to_snake(s: str) -> str:
    return s.replace("-", "_")


def slug_to_kebab(s: str) -> str:
    return s.replace("_", "-")


def detect_string_type(
    string: str,
) -> typing.Literal[
    "url-image",
    "url-video",
    "url",
    "uuid",
    "base64-encoded-string",
    "email-address",
    "html",
    "domain-name",
    "phone-number",
    "json-string",
    "javascript-snippet",
    "date-string",
    "timestamp-string",
    "camelCase",
    "snake_case",
    "kebab-case",
    "unknown",
]:
    # Check for URLs
    if re.match(r"^https?://", string):
        if re.match(r"\.(jpeg|jpg|png|gif|bmp)$", string):
            return "url-image"
        elif re.match(r"\.(mp4|webm|ogv)$", string):
            return "url-video"
        else:
            return "url"

    # Check for UUIDs
    if RE_UUID.match(string):
        return "uuid"

    # # Check for base64-encoded strings
    try:
        if base64.b64encode(base64.b64decode(string)).decode("ascii") == string:
            return "base64-encoded-string"
    except Exception:
        pass
    # if re.match(r'^(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?$', string):
    #   return 'base64-encoded-string'

    # Check for email addresses
    if RE_EMAIL.match(string):
        return "email-address"

    if RE_HTML.match(string):
        return "html"

    # Check for domain names
    if RE_DOMAIN_NAMES.match(string):
        return "domain-name"

    # Check for phone numbers
    if RE_PHONE_NUMBER.match(string):
        return "phone-number"

    # Check for JSON strings
    try:
        orjson.loads(string)
        return "json-string"
    except ValueError:
        pass

    # Check for JavaScript snippets
    if RE_JAVASCRIPT.match(string):
        return "javascript-snippet"

    # Check for date and timestamp strings
    try:
        datetime.datetime.strptime(string, "%Y-%m-%d")
        return "date-string"
    except ValueError:
        pass
    try:
        parse_timestamp(string, raise_error=True)
        return "timestamp-string"
    except Exception:
        pass

    # Check for snake_case (contains underscores, no uppercase)
    if re.match(r"^[a-z][a-z0-9_]*$", string) and "_" in string:
        return "snake_case"

    # Check for kebab-case (contains hyphens, no uppercase)
    if re.match(r"^[a-z][a-z0-9-]*$", string) and "-" in string:
        return "kebab-case"

    # Check for camelCase (contains lowercase and uppercase, no spaces/special chars)
    if (
        re.match(r"^[a-zA-Z][a-zA-Z0-9]*$", string)
        and re.search(r"[A-Z]", string)
        and re.search(r"[a-z]", string)
    ):
        return "camelCase"

    return "unknown"


# models
def encode_base32(data: str | bytes | int) -> str:
    """
    Encode data into a Base32 string.
    Accepts strings, bytes, or integers.
    Uses the RFC4648 alphabet: A-Z, 2-7
    """
    if isinstance(data, str):
        # Convert string to bytes, then to integer
        data = data.encode("utf-8")

    if isinstance(data, bytes):
        # Convert bytes to integer
        n = int.from_bytes(data, "big")
    elif isinstance(data, int):
        n = data
        if not 0 <= n < (1 << 64):
            raise ValueError("Integer input must be a 64-bit unsigned integer")
    else:
        raise TypeError("Input must be a string, bytes, or integer")

    # RFC4648 Base32 alphabet (A-Z, 2-7)
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"

    # Convert to base32 string
    result = ""
    if n == 0:
        return "A"

    while n:
        n, remainder = divmod(n, 32)
        result = alphabet[remainder] + result

    return result
