import typing
from pathlib import Path
import yaml
import re
import datetime

# Lazy import URL to avoid circular dependency
_URL = None


def _get_url():
    global _URL
    if _URL is None:
        from good_common.types import URL

        _URL = URL
    return _URL


try:
    from yaml import CDumper as Dumper
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Dumper, Loader  # type: ignore[assignment]


# Create a custom Dumper class
class CustomDumper(Dumper):
    pass


# Define how strings with newlines should be represented
def represent_str_with_style(dumper, data):
    if "\n" in data:
        return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")
    return dumper.represent_scalar("tag:yaml.org,2002:str", data)


# Special handlers for other types
def represent_url(dumper, data):
    return dumper.represent_scalar("tag:yaml.org,2002:str", str(data))


def represent_set(dumper, data):
    return dumper.represent_sequence("tag:yaml.org,2002:seq", sorted(list(data)))


def represent_datetime(dumper, data):
    return dumper.represent_scalar(
        "tag:yaml.org,2002:timestamp", data.isoformat(), style="plain"
    )


# Register the representers
CustomDumper.add_representer(str, represent_str_with_style)
# URL representer will be registered lazily when needed
CustomDumper.add_representer(set, represent_set)
CustomDumper.add_representer(datetime.datetime, represent_datetime)


# Function to register URL representer when first used
def _ensure_url_registered():
    URL = _get_url()
    if URL and URL not in CustomDumper.yaml_representers:
        CustomDumper.add_representer(URL, represent_url)


# Prevent aliases (references) in the YAML output
CustomDumper.ignore_aliases = lambda *args: True  # type: ignore[method-assign]


def normalize_unicode_and_newlines(data):
    """
    Recursively process data to normalize Unicode characters and ensure
    consistent newline representation
    """
    if isinstance(data, dict):
        return {k: normalize_unicode_and_newlines(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [normalize_unicode_and_newlines(item) for item in data]
    elif isinstance(data, str):
        # Replace escaped Unicode sequences with actual Unicode characters
        unicode_fixed = re.sub(
            r"\\u([0-9a-fA-F]{4})", lambda m: chr(int(m.group(1), 16)), data
        )

        # Ensure consistent newlines
        newline_fixed = unicode_fixed.replace("\\n", "\n")

        return newline_fixed
    return data


def yaml_load(path) -> typing.Any:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.load(f, Loader=Loader)


def yaml_dumps(data: typing.Any, sort_keys: bool = False, **kwargs) -> str:
    # Ensure URL representer is registered if needed
    _ensure_url_registered()

    # Pre-process the data to normalize Unicode and newlines
    processed_data = normalize_unicode_and_newlines(data)

    # Make sure we're using UTF-8 encoding and proper newlines
    kwargs.setdefault("allow_unicode", True)
    kwargs.setdefault("default_flow_style", False)

    return typing.cast(
        str,
        yaml.dump(processed_data, Dumper=CustomDumper, sort_keys=sort_keys, **kwargs),
    )


def yaml_loads(data: str) -> typing.Any:
    return yaml.load(data, Loader=Loader)


def yaml_dump(path: str | Path, data: typing.Any, sort_keys=False, **kwargs) -> None:
    # Ensure URL representer is registered if needed
    _ensure_url_registered()

    # Pre-process the data to normalize Unicode and newlines
    processed_data = normalize_unicode_and_newlines(data)

    # Make sure we're using UTF-8 encoding and proper newlines
    kwargs.setdefault("allow_unicode", True)
    kwargs.setdefault("default_flow_style", False)

    with open(path, "w", encoding="utf-8") as f:
        return yaml.dump(
            processed_data, f, Dumper=CustomDumper, sort_keys=sort_keys, **kwargs
        )
