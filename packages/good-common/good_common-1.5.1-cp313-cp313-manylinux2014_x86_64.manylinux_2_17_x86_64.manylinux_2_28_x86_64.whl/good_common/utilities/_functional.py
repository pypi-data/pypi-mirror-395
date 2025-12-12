import re
import typing
from collections.abc import Mapping, Sequence
from functools import reduce
from typing import Callable, TypeVar, overload, cast

from loguru import logger

T = TypeVar("T")
T1 = TypeVar("T1")
T2 = TypeVar("T2")
T3 = TypeVar("T3")
T4 = TypeVar("T4")
T5 = TypeVar("T5")
T6 = TypeVar("T6")


@overload
def simple_pipeline(f1: Callable[[T], T1]) -> Callable[[T], T1]: ...


@overload
def simple_pipeline(
    f1: Callable[[T], T1], f2: Callable[[T1], T2]
) -> Callable[[T], T2]: ...


@overload
def simple_pipeline(
    f1: Callable[[T], T1], f2: Callable[[T1], T2], f3: Callable[[T2], T3]
) -> Callable[[T], T3]: ...


@overload
def simple_pipeline(
    f1: Callable[[T], T1],
    f2: Callable[[T1], T2],
    f3: Callable[[T2], T3],
    f4: Callable[[T3], T4],
) -> Callable[[T], T4]: ...


@overload
def simple_pipeline(
    f1: Callable[[T], T1],
    f2: Callable[[T1], T2],
    f3: Callable[[T2], T3],
    f4: Callable[[T3], T4],
    f5: Callable[[T4], T5],
) -> Callable[[T], T5]: ...


@overload
def simple_pipeline(*functions: Callable) -> Callable: ...


def simple_pipeline(*functions: Callable) -> Callable:  # type: ignore[misc]
    """Create a simple_pipeline function from a sequence of callables.

    The returned function's input type matches the first function's input type,
    and the output type matches the last function's output type.

    Args:
        *functions: Variable number of callables to compose left-to-right

    Returns:
        A single callable that applies all functions in sequence

    Example:
        >>> process = simple_pipeline(str.lower, str.strip, len)
        >>> process("  HELLO  ")
        5

        >>> # With type inference
        >>> transform = simple_pipeline(
        ...     lambda x: x.split(),      # str -> list[str]
        ...     lambda x: [w.upper() for w in x],  # list[str] -> list[str]
        ...     len                        # list[str] -> int
        ... )
        >>> transform("hello world")
        2
    """
    if not functions:
        return lambda x: x

    def piped(initial):
        return reduce(lambda x, f: f(x), functions, initial)

    # Copy some metadata from the first function
    piped.__name__ = f"simple_pipeline({', '.join(f.__name__ for f in functions if hasattr(f, '__name__'))})"

    return piped


def try_chain(
    fns: list[typing.Callable[..., T]], fail=False, default_value: T | None = None
) -> typing.Callable[..., T | None]:
    def _try_chain(value):
        for fn in fns:
            try:
                return fn(value)
            except Exception:
                continue
        if fail:
            raise ValueError(f"Could not process {value}")
        return default_value

    return _try_chain


X = typing.TypeVar("X")


def deep_attribute_get(
    obj: typing.Any,
    path: str,
    default: typing.Any = None,
    debug: bool = False,
    return_paths: bool = False,
) -> typing.Union[
    typing.Any, typing.List[typing.Any], typing.List[typing.Tuple[typing.Any, str]]
]:
    segments = re.split(r"\.(?![^\[]*\])", path)
    if debug:
        logger.debug(f"Path segments: {segments}")
    result = _traverse(obj, segments, default, debug, "", return_paths)
    flattened = _flatten_and_filter(result, return_paths)

    if return_paths:
        filtered = [(value, path) for value, path in flattened if value is not None]
        return filtered[0] if len(filtered) == 1 else (filtered or None)
    else:
        filtered = [value for value in flattened if value is not None]
        return filtered[0] if len(filtered) == 1 else None


def _traverse(
    obj: typing.Any,
    segments: list[str],
    default: typing.Any,
    debug: bool,
    current_path: str,
    return_paths: bool,
) -> typing.Any:
    if not segments:
        return (obj, current_path) if return_paths else obj

    current_segment = segments[0]
    remaining_segments = segments[1:]

    if debug:
        print(f"Current segment: {current_segment}")
        print(f"Object type: {type(obj)}")

    if current_segment == "*":
        if isinstance(obj, Mapping):
            return [
                _traverse(
                    value,
                    remaining_segments,
                    default,
                    debug,
                    f"{current_path}.{key}",
                    return_paths,
                )
                for key, value in obj.items()
            ]
        elif isinstance(obj, Sequence) and not isinstance(obj, (str, bytes)):
            return [
                _traverse(
                    item,
                    remaining_segments,
                    default,
                    debug,
                    f"{current_path}[{i}]",
                    return_paths,
                )
                for i, item in enumerate(obj)
            ]
        else:
            if debug:
                print(f"Wildcard '*' not applicable for object of type {type(obj)}")
            return default

    if "[" in current_segment and "]" in current_segment:
        key, index = current_segment.split("[", 1)
        index = index.rstrip("]")
        if key:
            obj = anyget(obj, key, default)
            current_path = f"{current_path}.{key}" if current_path else key
            if obj is default:
                if debug:
                    print(f"Key '{key}' not found in object")
                return default
        if index == "*":
            if isinstance(obj, Sequence) and not isinstance(obj, (str, bytes)):
                return [
                    _traverse(
                        item,
                        remaining_segments,
                        default,
                        debug,
                        f"{current_path}[{i}]",
                        return_paths,
                    )
                    for i, item in enumerate(obj)
                ]
            else:
                if debug:
                    print(
                        f"Wildcard '[*]' not applicable for object of type {type(obj)}"
                    )
                return default
        try:
            obj = obj[int(index)]
            current_path = f"{current_path}[{index}]"
        except (IndexError, ValueError, TypeError):
            if debug:
                print(f"Invalid index {index} for object of type {type(obj)}")
            return default
    else:
        if isinstance(obj, Mapping):
            matching_keys = [
                k for k in obj.keys() if re.fullmatch(current_segment, str(k))
            ]
            if debug:
                print(f"Matching keys for pattern '{current_segment}': {matching_keys}")
            if len(matching_keys) == 1:
                obj = obj[matching_keys[0]]
                current_path = (
                    f"{current_path}.{matching_keys[0]}"
                    if current_path
                    else matching_keys[0]
                )
            elif len(matching_keys) > 1:
                return [
                    _traverse(
                        obj[k],
                        remaining_segments,
                        default,
                        debug,
                        f"{current_path}.{k}",
                        return_paths,
                    )
                    for k in matching_keys
                ]
            else:
                if debug:
                    print(f"No matching keys found for pattern '{current_segment}'")
                return default
        # if isinstance(obj, Mapping):
        #     matching_keys = [k for k in obj.keys() if re.match(current_segment, str(k))]
        #     if debug:
        #         print(f"Matching keys for pattern '{current_segment}': {matching_keys}")
        #     if len(matching_keys) == 1:
        #         obj = obj[matching_keys[0]]
        #         current_path = (
        #             f"{current_path}.{matching_keys[0]}"
        #             if current_path
        #             else matching_keys[0]
        #         )
        #     elif len(matching_keys) > 1:
        #         return [
        #             _traverse(
        #                 obj[k],
        #                 remaining_segments,
        #                 default,
        #                 debug,
        #                 f"{current_path}.{k}",
        #                 return_paths,
        #             )
        #             for k in matching_keys
        #         ]
        #     else:
        #         if debug:
        #             print(f"No matching keys found for pattern '{current_segment}'")
        #         return default
        else:
            obj = anyget(obj, current_segment, default)
            current_path = (
                f"{current_path}.{current_segment}" if current_path else current_segment
            )

        if obj is default:
            if debug:
                print(f"Segment '{current_segment}' not found in object")
            return default

    return _traverse(
        obj, remaining_segments, default, debug, current_path, return_paths
    )


def _flatten_and_filter(result: typing.Any, return_paths: bool) -> typing.List:
    if isinstance(result, list):
        return [
            item
            for sublist in [
                _flatten_and_filter(i, return_paths) for i in result if i is not None
            ]
            for item in sublist
        ]
    if return_paths:
        return [result] if result[0] is not None else []
    return [result] if result is not None else []


def anyget(obj: typing.Any, key: str, default: X | None = None) -> T | X | None:
    if isinstance(obj, Mapping):
        return cast(T | X | None, obj.get(key, default))
    elif hasattr(obj, key):
        return cast(T | X | None, getattr(obj, key))
    return default


VT = typing.TypeVar("VT")


def anyset(obj: VT, key: str, value: typing.Any) -> VT:
    if isinstance(obj, dict):
        obj[key] = value
    else:
        setattr(obj, key, value)
    return obj


def deep_attribute_set(obj: typing.Any, path: str, value: typing.Any) -> typing.Any:
    if "." not in path:
        return anyset(obj, path, value)
    key, rest = path.split(".", 1)
    return deep_attribute_set(anyget(obj, key, {}), rest, value)


def set_defaults(__base: dict | None = None, **kwargs):
    if not __base:
        __base = {}
    for k, v in kwargs.items():
        if k not in __base:
            __base[k] = v
    return __base


def filter_nulls(obj: T) -> T:
    if isinstance(obj, dict):
        return {  # type: ignore[return-value]
            k: v
            for k, v in ((k, filter_nulls(v)) for k, v in obj.items())
            if v not in (None, {}, [])
        }
    elif isinstance(obj, list):
        return [v for v in (filter_nulls(v) for v in obj) if v not in (None, {}, [])]  # type: ignore[return-value]
    else:
        return obj


def dict_without_keys(
    d: dict,
    keys: list[str],
) -> dict:
    return {k: v for k, v in d.items() if k not in keys} if d else {}


def function_args_dict(
    function: typing.Callable,
    args: tuple = (),
    kwargs: dict = {},
):
    import inspect

    sig = inspect.signature(function)
    bound_args = sig.bind(*args, **kwargs)
    bound_args.apply_defaults()
    return bound_args.arguments
