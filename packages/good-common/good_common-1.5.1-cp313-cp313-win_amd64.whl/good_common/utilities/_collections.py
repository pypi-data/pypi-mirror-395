from __future__ import annotations

import collections
import dataclasses
import glob
import typing
from collections.abc import Iterable, MutableMapping
from jsonpath_rust_bindings import Finder

import farmhash
import jsonlines
import orjson
import slugify
from box import Box
from pydantic import BaseModel
from pydantic.main import IncEx
from ._functional import filter_nulls, try_chain

# Version detection for jsonpath_rust_bindings
import importlib.metadata
import re as _re


def _get_jsonpath_version():
    """Get the version of jsonpath_rust_bindings as a tuple."""
    try:
        version_str = importlib.metadata.version("jsonpath_rust_bindings")
        # Parse version string like "1.0.0" or "0.7.0"
        match = _re.match(r"^(\d+)\.(\d+)\.(\d+)", version_str)
        if match:
            return tuple(int(x) for x in match.groups())
    except Exception:
        pass
    # Default to assuming old version if we can't detect
    return (0, 7, 0)


_JSONPATH_VERSION = _get_jsonpath_version()
_IS_JSONPATH_V1_PLUS = _JSONPATH_VERSION[0] >= 1

# Type aliases
DictLike = typing.Union[dict, "DotDict"]
D = typing.TypeVar("D", bound=dict | MutableMapping)
TKey = str | int
TKeys = tuple[TKey, ...]
TVal = str | int | float | bool | None
JSONLike = dict[str, typing.Any] | list[typing.Any]

# Dictionary operations

T = typing.TypeVar("T", bound=dict | list)


def sort_object_keys(obj: T) -> T:
    if isinstance(obj, dict):
        return {k: sort_object_keys(v) for k, v in sorted(obj.items())}  # type: ignore[return-value]
    if isinstance(obj, list):
        return [sort_object_keys(i) for i in obj]  # type: ignore[return-value]
    return obj


def sort_if_sortable(obj: T) -> T:
    try:
        return sorted(obj)  # type: ignore[return-value]
    except TypeError:
        return obj


_fallback_serializer = try_chain(
    [
        lambda data: farmhash.hash64(
            orjson.dumps(
                sort_object_keys(filter_nulls(data)), default=serialize
            ).decode()
        ),
        lambda data: farmhash.hash64(str(hash(data))),
    ]
)


def hash_serialize(data: typing.Any) -> typing.Any:
    if hasattr(data, "__hash__") and getattr(data, "__hash__"):
        return hash(data)
    elif isinstance(data, BaseModel):
        return farmhash.hash64(
            orjson.dumps(
                sort_object_keys(filter_nulls(data.model_dump(mode="json"))),
                default=hash_serialize,
            ).decode()
        )
    elif isinstance(data, dict):
        return farmhash.hash64(
            orjson.dumps(
                sort_object_keys(filter_nulls(data)), default=hash_serialize
            ).decode()
        )
    elif isinstance(data, list):
        return farmhash.hash64(
            orjson.dumps(
                sort_if_sortable(filter_nulls(data)), default=hash_serialize
            ).decode()
        )
    elif isinstance(data, (tuple, set)):
        return hash_serialize(sort_if_sortable(filter_nulls(list(data))))
    else:
        return _fallback_serializer(data)


def serialize(data: typing.Any) -> typing.Any:
    """
    Serialize
    """
    if hasattr(data, "__hash__") and getattr(data, "__hash__"):
        return hash(data)
    elif isinstance(data, dict):
        return farmhash.hash64(
            orjson.dumps(
                sort_object_keys(filter_nulls(data)), default=serialize
            ).decode()
        )
    elif isinstance(data, list):
        return farmhash.hash64(
            orjson.dumps(
                sort_if_sortable(filter_nulls(data)), default=serialize
            ).decode()
        )
    elif isinstance(data, (tuple, set)):
        return serialize(sort_if_sortable(filter_nulls(list(data))))
    elif isinstance(data, bytes):
        return hash(data)
    else:
        return str(data)


def object_farmhash(
    obj: BaseModel | typing.Any, exclude_keys: IncEx | None = None
) -> int:
    """
    Generate a consistent FarmHash64 hash from an object (include Pydantic models)

    :param obj: A Pydantic model instance
    :return: 64-bit FarmHash as an integer
    """

    if isinstance(obj, BaseModel):
        obj = obj.model_dump(mode="json", exclude_none=True, exclude=exclude_keys)

    serialized_data = hash_serialize(obj)
    data_str = str(serialized_data)
    return farmhash.hash64(data_str)


def merge_dicts(
    dicts: list[dict],
    keep_unique_values: bool = False,
    keep_unique_value_keys: list = [],
) -> dict:
    """
    Merge a list of dictionaries into a single dictionary.

    Args:
        dicts (list[dict]): List of dictionaries to merge.
        keep_unique_values (bool, optional): If True, keep all unique values for each key. Defaults to False.
        keep_unique_value_keys (list, optional): List of keys for which to keep unique values. Defaults to [].

    Returns:
        dict: Merged dictionary.
    """
    merged: typing.Dict = {}
    for d in deduplicate_dicts(dicts):
        for key, value in d.items():
            if isinstance(value, dict):
                if key in merged:
                    if isinstance(merged[key], list):
                        merged[key] = {k: v for k, v in enumerate(merged[key])}
                    merged_dict = merge_dicts(
                        [merged[key], value],
                        keep_unique_values=keep_unique_values,
                        keep_unique_value_keys=keep_unique_value_keys,
                    )
                    merged[key] = merged_dict
                else:
                    merged[key] = value
            elif isinstance(value, list):
                if key in merged:
                    for elem in value:
                        if elem not in merged[key]:
                            merged[key].append(elem)
                else:
                    merged[key] = value
            else:
                if value is not None and value != "":
                    if (
                        keep_unique_values and key in merged
                    ) or key in keep_unique_value_keys:
                        if not isinstance(merged[key], list):
                            merged[key] = [merged[key]]

                        if value not in merged[key]:
                            merged[key].append(value)

                        if len(merged[key]) == 1:
                            merged[key] = merged[key][0]
                    else:
                        merged[key] = value

    return {k: v for k, v in merged.items() if v is not None and v != ""}


def deduplicate_dicts(dicts: list[dict]) -> list[dict]:
    """
    Remove duplicate dictionaries from a list of dictionaries.

    Args:
        dicts (list[dict]): List of dictionaries to deduplicate.

    Returns:
        list[dict]: List of unique dictionaries.
    """
    new_dicts = []
    for d in dicts:
        if d not in new_dicts:
            new_dicts.append(d)
    return new_dicts


def clean_dict(d: typing.Union[dict, list, set]) -> typing.Union[dict, list]:
    """
    Convert defaultdict to plain dictionary recursively and handle unhashable types.

    Args:
        d (Union[dict, list, set]): Input data structure to clean.

    Returns:
        Union[dict, list]: Cleaned data structure.
    """
    if isinstance(d, dict):
        return {k: clean_dict(v) for k, v in d.items()}
    elif isinstance(d, (list, set)):
        return [clean_dict(v) for v in d]
    else:
        return d


def recursive_remove_nones(obj: dict) -> dict:
    """
    Recursively remove None values from a dictionary.

    Args:
        obj (dict): Input dictionary.

    Returns:
        dict: Dictionary with None values removed.
    """
    _new = {}
    for k, v in obj.items():
        if isinstance(v, dict):
            _new[k] = recursive_remove_nones(v)
        elif v is not None:
            _new[k] = v
    return _new


def set_defaults(__base: dict | None = None, **kwargs) -> dict:
    """
    Set default values in a dictionary.

    Args:
        __base (dict | None, optional): Base dictionary to update. Defaults to None.
        **kwargs: Key-value pairs to set as defaults.

    Returns:
        dict: Updated dictionary with default values.
    """
    if not __base:
        __base = {}
    for k, v in kwargs.items():
        if v:
            __base[k] = v
    return __base


# List operations


def merge_lists(lists: list[list]) -> list:
    """
    Merge multiple lists, removing duplicates.

    Args:
        lists (list[list]): List of lists to merge.

    Returns:
        list: Merged list with unique elements.
    """
    merged = []
    for _list in lists:
        for elem in _list:
            if elem not in merged:
                merged.append(elem)
    return merged


def flatten_list(lst: list) -> list:
    """
    Flatten a list of lists.

    Args:
        lst (list): List to flatten.

    Returns:
        list: Flattened list.
    """
    flattened = []
    for item in lst:
        if isinstance(item, list):
            flattened.extend(flatten_list(item))
        else:
            flattened.append(item)
    return flattened


# Object conversion and manipulation


def recursive_to_dict(o: typing.Any) -> typing.Any:
    """
    Recursively convert an object to a dictionary.

    Args:
        o (typing.Any): Object to convert.

    Returns:
        typing.Any: Converted object.
    """
    if isinstance(o, dict):
        return {k: recursive_to_dict(v) for k, v in o.items()}
    elif hasattr(o, "__dict__"):
        return recursive_to_dict(o.__dict__)
    elif isinstance(o, list):
        return [recursive_to_dict(v) for v in o]
    else:
        return o


def to_dict(obj: typing.Any) -> dict:
    """
    Convert various object types to a dictionary.

    Args:
        obj (typing.Any): Object to convert.

    Returns:
        dict: Dictionary representation of the object.
    """
    if hasattr(obj, "model_export"):
        return typing.cast(dict[str, typing.Any], obj.model_export())
    elif dataclasses.is_dataclass(obj):
        if isinstance(obj, type):
            # If obj is a dataclass type, not an instance
            return {
                field.name: getattr(field, "default", None)
                for field in dataclasses.fields(obj)
            }
        else:
            # If obj is a dataclass instance
            return dataclasses.asdict(obj)
    elif hasattr(obj, "json"):
        return typing.cast(dict[str, typing.Any], orjson.loads(obj.json()))
    elif hasattr(obj, "dict"):
        return typing.cast(dict[str, typing.Any], obj.dict())
    elif hasattr(obj, "as_dict"):
        return typing.cast(dict[str, typing.Any], obj.as_dict())
    elif hasattr(obj, "_asdict"):
        return typing.cast(dict[str, typing.Any], obj._asdict())
    elif hasattr(obj, "to_dict"):
        return typing.cast(dict[str, typing.Any], obj.to_dict())
    else:
        raise TypeError(f"Object of type {type(obj)} is not convertible to dict")


def map_object(obj: dict, **mappers) -> dict:
    """
    Apply functions to specific keys in a dictionary.

    Args:
        obj (dict): Input dictionary.
        **mappers: Functions to apply to specific keys.

    Returns:
        dict: Dictionary with mapped values.
    """
    _new = {}
    for k, v in obj.items():
        if k in mappers and v:
            if callable(mappers[k]):
                _v = mappers[k](v)
                if _v:
                    _new[k] = _v
                else:
                    _new[k] = v
            else:
                _new[k] = v
        else:
            _new[k] = v
    return _new


# JSON and file operations


def get_records_from_glob(
    path: str, limit: int | None = None, filters: list[typing.Callable] = []
) -> list[dict]:
    """
    Get records from JSON files matching a glob pattern.

    Args:
        path (str): Glob pattern for JSON files.
        limit (int | None, optional): Maximum number of records to return. Defaults to None.
        filters (list[typing.Callable], optional): List of filter functions to apply. Defaults to [].

    Returns:
        list[dict]: List of records from JSON files.
    """
    records = []
    for file in glob.glob(path):
        for record in jsonlines.open(file, loads=orjson.loads):
            if all([f(record) for f in filters]) or len(filters) == 0:
                records.append(record)
            if limit and len(records) >= limit:
                return records

    return records


def get_data_from_records(
    records: list[dict], path: str
) -> typing.Generator[typing.Any, typing.Any, None]:
    """
    Get nested data from a list of records using a dot-separated path.

    Args:
        records (list[dict]): List of records to search.
        path (str): Dot-separated path to the desired data.

    Yields:
        typing.Any: Nested data from records.
    """
    for record in records:
        o = recursive_get(record, *path.split("."))
        if o:
            yield o


def expand_nested_json(obj: dict) -> dict:
    """
    Expand nested JSON strings within a dictionary.

    Args:
        obj (dict): Dictionary containing nested JSON strings.

    Returns:
        dict: Dictionary with expanded nested JSON.

    Raises:
        ValueError: If the expanded object is not a dictionary.
    """

    def _expand_nested_json(obj: JSONLike) -> JSONLike:
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, str):
                    try:
                        loaded = orjson.loads(v)
                    except ValueError:
                        obj[k] = v
                        continue
                    if isinstance(loaded, (dict, list)):
                        obj[k] = _expand_nested_json(loaded)
                    else:
                        obj[k] = loaded
                else:
                    if isinstance(v, (dict, list)):
                        obj[k] = _expand_nested_json(v)
                    else:
                        obj[k] = v
        elif isinstance(obj, list):
            for i, v in enumerate(obj):
                if isinstance(v, str):
                    try:
                        loaded = orjson.loads(v)
                    except ValueError:
                        obj[i] = v
                        continue
                    if isinstance(loaded, (dict, list)):
                        obj[i] = _expand_nested_json(loaded)
                    else:
                        obj[i] = loaded
                else:
                    if isinstance(v, (dict, list)):
                        obj[i] = _expand_nested_json(v)
                    else:
                        obj[i] = v
        return obj

    _obj = _expand_nested_json(obj)
    if isinstance(_obj, dict):
        return _obj
    else:
        raise ValueError(f"Expanded object {_obj=} not a dictionary")


# Nested data access and manipulation


def recursive_default(obj: dict, *keys) -> typing.Any:
    """
    Get a value from nested dictionaries using multiple keys.

    Args:
        obj (dict): Dictionary to search.
        *keys: Keys to search for.

    Returns:
        typing.Any: Value found or None if not found.
    """
    for i, key in enumerate(keys):
        if isinstance(obj, dict):
            if key in obj:
                obj = obj[key]
            else:
                # If it's the last key and not found, return the entire object
                return obj if i == len(keys) - 1 else None
        else:
            return None
    return obj


def recursive_get(obj: dict | None, *keys) -> typing.Any:
    """
    Get a value from nested dictionaries using multiple keys.

    Args:
        obj (dict | None): Dictionary to search.
        *keys: Keys to search for.

    Returns:
        typing.Any: Value found or None if not found.
    """
    if obj is None:
        return None
    if len(keys) == 0:
        return obj

    if isinstance(keys[0], list):
        _obj = recursive_default(obj, *keys[0])
        if isinstance(_obj, dict):
            return recursive_get(_obj, *keys[1:])
        else:
            return _obj

    if keys[0] in obj:
        return recursive_get(obj.get(keys[0]), *keys[1:])
    return None


def recursive_convert_lists(obj: dict | list | typing.Any) -> dict | list | typing.Any:
    """
    Convert nested objects with numeric string keys to lists.

    Args:
        obj (dict): Dictionary to convert.

    Returns:
        dict: Dictionary with converted nested objects.
    """
    # if isinstance(obj, dict):
    #     for k, v in obj.items():
    #         if isinstance(v, dict) and all(
    #             [isinstance(k, str) and k.isdigit() for k in v.keys()]
    #         ):
    #             obj[k] = [recursive_convert_lists(v) for v in v.values()]
    #         elif isinstance(v, dict):
    #             obj[k] = recursive_convert_lists(v)
    # return obj
    if isinstance(obj, dict):
        if all(isinstance(k, str) and k.isdigit() for k in obj.keys()):
            return [
                recursive_convert_lists(v)
                for _, v in sorted(obj.items(), key=lambda x: int(x[0]))
            ]
        return {k: recursive_convert_lists(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [recursive_convert_lists(v) for v in obj]
    return obj


# Index and deindex operations


def index_object(obj: dict, keys_as_tuples: bool = False) -> dict:
    def _index_object(obj, path=None):
        if path is None:
            path = []
        if isinstance(obj, dict):
            for k, v in obj.items():
                yield from _index_object(v, path + [k])
        elif isinstance(obj, list):
            for i, v in enumerate(obj):
                if isinstance(v, (dict, list)):
                    yield from _index_object(v, path + [f"[{i}]"])
                else:
                    yield (tuple(path + [f"[{i}]"]), v)
        else:
            yield (tuple(path), obj)

    indexed = {path: value for path, value in _index_object(obj)}
    if not keys_as_tuples:
        return {path_tuple_to_string(path): value for path, value in indexed.items()}
    return indexed


def deindex_object(obj: dict[str, TVal]) -> TReturn:
    def _set_nested(
        result: dict[str, typing.Any],
        keys: list[str],
        value: TVal,
    ) -> dict[str, typing.Any]:
        current: dict[str, typing.Any] = result
        for i, key in enumerate(keys[:-1]):
            if key.startswith("[") and key.endswith("]"):
                index = int(key[1:-1])
                if not isinstance(current, dict):
                    current = {}
                    if i == 0:
                        result = current
                    else:
                        result[keys[i - 1]] = current
                if str(index) not in current:
                    current[str(index)] = {}
                current = current[str(index)]
            else:
                if key not in current:
                    current[key] = {}
                current = current[key]

        last_key = keys[-1]
        if last_key.startswith("[") and last_key.endswith("]"):
            index = int(last_key[1:-1])
            current[str(index)] = value
        else:
            current[last_key] = value
        return result

    def _dict_to_list(
        d: dict[str, typing.Any] | list[typing.Any] | TVal,
    ) -> TReturn:
        if isinstance(d, dict):
            if all(k.isdigit() for k in d.keys()):
                return typing.cast(
                    TReturn, [_dict_to_list(d[str(i)]) for i in range(len(d))]
                )
            return typing.cast(TReturn, {k: _dict_to_list(v) for k, v in d.items()})
        if isinstance(d, list):
            return typing.cast(TReturn, [_dict_to_list(v) for v in d])
        return typing.cast(TReturn, d)

    result: dict[str, typing.Any] = {}
    for path, value in obj.items():
        keys = path.replace("]", "").replace("[", ".").split(".")
        result = _set_nested(result, keys, value)

    return _dict_to_list(result)


def index_objects(objs: list) -> list[dict]:
    """
    Create indexed representations of a list of nested objects.

    Args:
        objs (list): List of objects to index.

    Returns:
        list[dict]: List of indexed representations of the objects.
    """
    return [index_object(obj) for obj in objs]


def deindex_objects(objs: list) -> list[TReturn]:
    """
    Convert a list of indexed objects back to their nested forms.

    Args:
        objs (list): List of indexed objects to convert.

    Returns:
        list[dict]: List of nested forms of the objects.
    """
    return [deindex_object(obj) for obj in objs]


# Helper functions for index/deindex operations


def _handle_serialized_key(key: str) -> str:
    """
    Handle serialized keys in indexed objects.

    Args:
        key (str): Key to handle.

    Returns:
        str: Processed key.
    """
    if "{" in key:
        try:
            d = orjson.loads(key)
            _key = ""
            for k, v in index_object(d).items():
                _key += f"{k}_{v}__"
            return _key
        except Exception:
            return slugify.slugify(key, separator="_")
    else:
        return key


def path_tuple_to_string(path: tuple) -> str:
    """
    Convert a path tuple to a string representation.

    Args:
        path (tuple): Path tuple to convert.

    Returns:
        str: String representation of the path.
    """
    _path = ".".join(
        f"[{i}]" if isinstance(i, int) else _handle_serialized_key(i) for i in path
    )
    return _path.replace(".[", "[")


def path_string_to_tuple(path: str) -> tuple:
    """
    Convert a string path to a tuple representation.

    Args:
        path (str): String path to convert.

    Returns:
        tuple: Tuple representation of the path.
    """
    # return tuple(int(i[1:-1]) if i.startswith("[") else i for i in path.split("."))
    return tuple(
        int(i[1:-1]) if i.startswith("[") and i.endswith("]") else i
        for i in path.split(".")
    )


TReturn = dict[TKey, typing.Any] | list[typing.Any] | str | int | float | bool | None


def _deindex_object(obj: dict[tuple[TKey, ...], TVal]) -> TReturn:
    result: dict[TKey, typing.Any] = {}
    for key, value in obj.items():
        current = result
        for i, k in enumerate(key[:-1]):
            if isinstance(k, str) and k.startswith("[") and k.endswith("]"):
                # This is a list index
                parent_key = key[i - 1]
                if parent_key not in current:
                    current[parent_key] = []
                index = int(k[1:-1])
                while len(current[parent_key]) <= index:
                    current[parent_key].append({})
                current = current[parent_key][index]
            else:
                if k not in current:
                    current[k] = {}
                current = current[k]
        last_key = key[-1]
        if (
            isinstance(last_key, str)
            and last_key.startswith("[")
            and last_key.endswith("]")
        ):
            parent_key = key[-2]
            index = int(last_key[1:-1])
            if parent_key not in current:
                current[parent_key] = []
            while len(current[parent_key]) <= index:
                current[parent_key].append(None)
            current[parent_key][index] = value
        else:
            current[last_key] = value
    return result


def _set_nested_dict(
    d: dict[TKey, typing.Any], keys: tuple[TKey, ...], value: typing.Any
) -> None:
    """
    Set a value in a nested dictionary using a tuple of keys.

    Args:
        d (dict[TKey, typing.Any]): Dictionary to modify.
        keys (tuple[TKey, ...]): Tuple of keys representing the path.
        value (typing.Any): Value to set.

    Raises:
        TypeError: If a non-integer key is used with a list.
    """
    for key in keys[:-1]:
        if isinstance(d, list):
            if not isinstance(key, int):
                raise TypeError(
                    f"List indices must be integers, not {type(key).__name__}"
                )
            while len(d) <= key:
                d.append({})
            if not isinstance(d[key], (dict, list)):
                d[key] = {}
            d = d[key]
        else:
            d = d.setdefault(key, {})

    if isinstance(d, list):
        if not isinstance(keys[-1], int):
            raise TypeError(
                f"List indices must be integers, not {type(keys[-1]).__name__}"
            )
        while len(d) <= keys[-1]:
            d.append({})
        d[keys[-1]] = value
    else:
        d[keys[-1]] = value


def _numeric_dicts_to_list(d: dict[TKey, TVal] | TVal) -> TReturn:
    """
    Convert numeric dictionaries to lists recursively.

    Args:
        d (dict[TKey, TVal] | TVal): Dictionary or value to convert.

    Returns:
        TReturn: Converted structure, which can be:
            - A dictionary with string or int keys and any values
            - A list of any values
            - A primitive value (str, int, float, bool, or None)
    """
    if isinstance(d, dict):
        if all(isinstance(k, str) and k.isdigit() for k in d.keys()):
            return [_numeric_dicts_to_list(d[str(i)]) for i in range(len(d))]
        return {k: _numeric_dicts_to_list(v) for k, v in d.items()}
    elif isinstance(d, list):
        return [_numeric_dicts_to_list(item) for item in d]
    else:
        return d


# Tree-like defaultdict
# ruff:  noqa: E731
tree: typing.Callable[[], collections.defaultdict] = lambda: collections.defaultdict(
    tree
)


def recursive_defaultdict_to_dict(obj: collections.defaultdict) -> dict:
    """
    Convert a recursive defaultdict to a regular dictionary.

    Args:
        obj (collections.defaultdict): Recursive defaultdict to convert.

    Returns:
        dict: Regular dictionary representation.
    """
    if isinstance(obj, collections.defaultdict):
        return {k: recursive_defaultdict_to_dict(v) for k, v in obj.items()}
    else:
        return obj


def convert_index_object_to_dict(index):
    result = tree()
    for path, val in index:
        d = result
        for element in path:
            d = d[element]
        d = val
    return result


# DotDict implementation
class DotDict(MutableMapping):
    def __init__(self, init_dict: DictLike | None = None, **kwargs: typing.Any):
        self.__dict__["_data"] = {}
        if init_dict:
            self.update(init_dict)
        self.update(kwargs)

    def __getattr__(self, key: str) -> typing.Any:
        return self[key]

    def __setattr__(self, key: str, value: typing.Any) -> None:
        self[key] = value

    def __getitem__(self, key: str) -> typing.Any:
        return self._data[key]

    def __setitem__(self, key: str, value: typing.Any) -> None:
        self._data[key] = self._convert(value)

    def __delitem__(self, key: str) -> None:
        del self._data[key]

    def __iter__(self) -> typing.Iterator[str]:
        return iter(self._data)

    def __len__(self) -> int:
        return len(self._data)

    def __repr__(self) -> str:
        return f"DotDict({self._data})"

    def _convert(self, value: typing.Any) -> typing.Any:
        if isinstance(value, dict) and not isinstance(value, DotDict):
            return DotDict(value)
        elif isinstance(value, list):
            return [self._convert(v) for v in value]
        return value

    def update(self, other: typing.Any = None, **kwargs: typing.Any) -> None:  # type: ignore[override]
        if other is not None:
            for k, v in other.items():
                self[k] = v
        for k, v in kwargs.items():
            self[k] = v

    def to_dict(self) -> dict:
        def _to_dict(value):
            if isinstance(value, DotDict):
                return value.to_dict()
            elif isinstance(value, list):
                return [_to_dict(v) for v in value]
            return value

        return {k: _to_dict(v) for k, v in self._data.items()}


def find(json: dict, query: str):
    """
    Execute a JSONPath query on a JSON-like dictionary.

    Args:
        json: The JSON data to query
        query: JSONPath query string

    Returns:
        List of JsonPathResult objects
    """
    return Finder(json).find(query)


def find_non_empty(json: dict, query: str):
    """
    Execute a JSONPath query and filter out empty/null results.

    Automatically handles both pre-1.0 and 1.0+ versions of jsonpath-rust-bindings.

    Args:
        json: The JSON data to query
        query: JSONPath query string

    Returns:
        List of JsonPathResult objects with non-empty data
    """
    if _IS_JSONPATH_V1_PLUS:
        # Version 1.0+: find_non_empty() was removed, filter manually
        results = Finder(json).find(query)

        # Filter out None, empty strings, empty lists, empty dicts
        # Keeping 0 and False as they are valid non-empty values
        def is_non_empty(data):
            if data is None:
                return False
            if isinstance(data, (str, list, dict)) and len(data) == 0:
                return False
            return True

        return [r for r in results if is_non_empty(r.data)]
    else:
        # Pre-1.0: Use the built-in find_non_empty method
        return Finder(json).find_non_empty(query)  # type: ignore[attr-defined]


def find_with_regex(json: dict, query: str, regex_replacements: dict | None = None):
    """
    Execute a JSONPath query with regex pattern matching support.

    Handles both pre-1.0 (with native regex support) and 1.0+ versions.

    Args:
        json: The JSON data to query
        query: JSONPath query string (regex patterns will be extracted)
        regex_replacements: Optional dict mapping field names to regex patterns

    Returns:
        List of JsonPathResult objects matching the patterns

    Example:
        # Pre-1.0: $.books[?(@.author ~= '.*Melville')]
        # 1.0+: find_with_regex(data, '$.books[*]', {'author': '.*Melville'})
    """
    if _IS_JSONPATH_V1_PLUS:
        # Version 1.0+: regex operator ~= is no longer supported, use post-filtering
        import re

        # Remove regex filters from query to get base query
        base_query = re.sub(r"\[\?\([^)]*~=[^)]*\)\]", "[*]", query)

        # Extract regex patterns from original query if not provided
        if regex_replacements is None:
            regex_replacements = {}
            # Pattern to extract field and regex from filter expressions
            pattern = r'\[\?\(@\.(\w+)\s*~=\s*[\'"]([^\'"]*)[\'"]\)\]'
            matches = re.findall(pattern, query)
            for field, regex_pattern in matches:
                regex_replacements[field] = regex_pattern

        # Get all results from base query
        results = Finder(json).find(base_query)

        # Filter results based on regex patterns
        if regex_replacements:
            filtered_results = []
            for result in results:
                data = result.data
                if isinstance(data, dict):
                    # Check if all regex patterns match
                    all_match = True
                    for field, pattern in regex_replacements.items():
                        if field in data:
                            value = str(data[field]) if data[field] is not None else ""
                            if not re.search(pattern, value):
                                all_match = False
                                break
                        else:
                            all_match = False
                            break
                    if all_match:
                        filtered_results.append(result)
                else:
                    filtered_results.append(result)
            return filtered_results

        return results
    else:
        # Pre-1.0: Use native regex support in JSONPath queries
        return Finder(json).find(query)


def find_or_empty(json: dict, query: str):
    """
    Execute a JSONPath query with consistent behavior across versions.

    In pre-1.0 versions, non-existent paths returned a single result with empty data.
    This function provides consistent behavior across versions.

    Args:
        json: The JSON data to query
        query: JSONPath query string

    Returns:
        List of JsonPathResult objects
    """
    results = Finder(json).find(query)

    # Both versions should return the same - just the results as-is
    # The behavioral difference was in the library itself, not our usage
    return results


# Helper functions for DotDict


def is_iterable(obj: typing.Any) -> typing.TypeGuard[Iterable]:
    """
    Check if an object is iterable (but not a string).

    Args:
        obj (typing.Any): Object to check.

    Returns:
        bool: True if the object is iterable and not a string, False otherwise.
    """
    return isinstance(obj, Iterable) and not isinstance(obj, (str, bytes))


def as_nested_dict(
    obj: MutableMapping[typing.Any, typing.Any] | Iterable[typing.Any],
    dct_class: type[MutableMapping] | typing.Callable[[], MutableMapping] = dict,
) -> MutableMapping[typing.Any, typing.Any] | typing.Any:
    """
    Convert a nested structure to the specified dictionary class.

    Args:
        obj (MutableMapping[typing.Any, typing.Any] | Iterable[typing.Any]): Object to convert.
        dct_class (type[MutableMapping] | Callable[[], MutableMapping], optional):
            Dictionary class or function that returns a new dictionary instance. Defaults to dict.

    Returns:
        MutableMapping[typing.Any, typing.Any] | typing.Any: Converted structure.
    """
    if isinstance(obj, (list, tuple, set)):
        return type(obj)(as_nested_dict(d, dct_class) for d in obj)
    elif isinstance(obj, Box):
        return dict(obj)
    elif isinstance(obj, MutableMapping):
        new_dict = dct_class() if callable(dct_class) else dct_class()
        for k, v in getattr(obj, "__dict__", obj).items():
            new_dict[k] = as_nested_dict(v, dct_class)
        return new_dict
    return obj


# Compound key operations


class CompoundKey(tuple):
    """A tuple subclass used for representing nested dictionary keys."""

    pass


def dict_to_flatdict(dct: DictLike, parent: CompoundKey | None = None) -> dict:
    """
    Convert a nested dictionary to a flat dictionary with compound keys.

    Args:
        dct (DictLike): Nested dictionary to flatten.
        parent (CompoundKey | None, optional): Parent key for recursive calls. Defaults to None.

    Returns:
        dict: Flattened dictionary with compound keys.
    """
    items: list[tuple[CompoundKey, typing.Any]] = []
    parent = parent or CompoundKey()
    for k, v in dct.items():
        k_parent = CompoundKey(parent + (k,))
        if isinstance(v, dict):
            items.extend(dict_to_flatdict(v, parent=k_parent).items())
        else:
            items.append((k_parent, v))
    return dict(items)


def flatdict_to_dict(dct: dict, dct_class: typing.Type[D] | None = None) -> D:
    """
    Convert a flat dictionary with compound keys back to a nested dictionary.

    Args:
        dct (dict): Flat dictionary with compound keys.
        dct_class (typing.Type[D] | None, optional): Dictionary class to use for the result. Defaults to None.

    Returns:
        D: Nested dictionary of the specified class.
    """
    result = typing.cast(D, (dct_class or dict)())
    for k, v in dct.items():
        if isinstance(k, CompoundKey):
            current_dict = result
            for ki in k[:-1]:
                current_dict = current_dict.setdefault(ki, (dct_class or dict)())
            current_dict[k[-1]] = v
        else:
            result[k] = v

    return result


# Utility function for flattening sequences
def flatten_seq(seq: Iterable) -> typing.Generator:
    """
    Flatten a nested sequence (e.g., list of lists) into a single level.

    Args:
        seq (Iterable): Nested sequence to flatten.

    Yields:
        typing.Any: Elements from the flattened sequence.

    Example:
        >>> list(flatten_seq([1, [2, 3, [4, 5]], 6]))
        [1, 2, 3, 4, 5, 6]
    """
    for item in seq:
        if isinstance(item, Iterable) and not isinstance(item, (str, bytes)):
            yield from flatten_seq(item)
        else:
            yield item
