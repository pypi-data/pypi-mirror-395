# cython: language_level=3
# cython: boundscheck=False
# cython: wraparound=False
# cython: cdivision=True
# cython: nonecheck=False
"""
Cython-optimized functional utility functions.
"""

import re
import typing
from collections.abc import Mapping, Sequence
cimport cython

# Import filter_nulls from collections (will be built separately)
# We'll define it here to avoid circular import


cpdef object deep_attribute_get(
    object obj,
    str path,
    object default=None,
    bint debug=False,
    bint return_paths=False
):
    """
    Get nested attributes using dot notation with wildcards.
    
    Optimized with:
    - Direct path parsing
    - Efficient traversal
    - Reduced regex compilation
    """
    cdef list segments = _split_path(path)
    cdef object result = _traverse(obj, segments, default, debug, "", return_paths)
    cdef list flattened = _flatten_and_filter(result, return_paths)
    
    if return_paths:
        filtered = [(value, path) for value, path in flattened if value is not None]
        return filtered[0] if len(filtered) == 1 else (filtered or None)
    else:
        filtered = [value for value in flattened if value is not None]
        return filtered[0] if len(filtered) == 1 else None


cdef list _split_path(str path):
    """Split path by dots not inside brackets."""
    # Use simple regex split
    return re.split(r'\.(?![^\[]*\])', path)


cdef object _traverse(
    object obj,
    list segments,
    object default,
    bint debug,
    str current_path,
    bint return_paths
):
    """Traverse object following path segments."""
    if not segments:
        return (obj, current_path) if return_paths else obj
    
    cdef str current_segment = segments[0]
    cdef list remaining_segments = segments[1:]
    cdef str key
    cdef object value
    cdef int i, index
    cdef list results
    
    if debug:
        print(f"Current segment: {current_segment}")
        print(f"Object type: {type(obj)}")
    
    # Handle wildcard
    if current_segment == "*":
        if isinstance(obj, Mapping):
            results = []
            for key, value in obj.items():
                new_path = f"{current_path}.{key}" if current_path else key
                results.append(
                    _traverse(value, remaining_segments, default, debug, new_path, return_paths)
                )
            return results
            
        elif isinstance(obj, Sequence) and not isinstance(obj, (str, bytes)):
            results = []
            for i, item in enumerate(obj):
                new_path = f"{current_path}[{i}]"
                results.append(
                    _traverse(item, remaining_segments, default, debug, new_path, return_paths)
                )
            return results
        else:
            return default
    
    # Handle bracketed indices
    if "[" in current_segment and "]" in current_segment:
        parts = current_segment.split("[", 1)
        key = parts[0]
        index_str = parts[1].rstrip("]")
        
        if key:
            obj = _anyget(obj, key, default)
            current_path = f"{current_path}.{key}" if current_path else key
            if obj is default:
                return default
        
        if index_str == "*":
            if isinstance(obj, Sequence) and not isinstance(obj, (str, bytes)):
                results = []
                for i, item in enumerate(obj):
                    new_path = f"{current_path}[{i}]"
                    results.append(
                        _traverse(item, remaining_segments, default, debug, new_path, return_paths)
                    )
                return results
            else:
                return default
        
        try:
            index = int(index_str)
            obj = obj[index]
            current_path = f"{current_path}[{index_str}]"
        except (IndexError, ValueError, TypeError):
            return default
    else:
        # Regular key access
        obj = _anyget(obj, current_segment, default)
        current_path = f"{current_path}.{current_segment}" if current_path else current_segment
        
        if obj is default:
            return default
    
    return _traverse(obj, remaining_segments, default, debug, current_path, return_paths)


cdef object _anyget(object obj, str key, object default):
    """Get attribute from object, dict, or return default."""
    if isinstance(obj, Mapping):
        return obj.get(key, default)
    elif hasattr(obj, key):
        return getattr(obj, key)
    return default


cdef list _flatten_and_filter(object result, bint return_paths):
    """Flatten nested results and filter out None values."""
    if isinstance(result, list):
        flattened = []
        for item in result:
            if item is not None:
                flattened.extend(_flatten_and_filter(item, return_paths))
        return flattened
    
    if return_paths:
        return [result] if result[0] is not None else []
    return [result] if result is not None else []


def simple_pipeline(*functions):
    """
    Create a pipeline function from a sequence of callables.
    
    Optimized with:
    - Direct function composition
    - Reduced overhead
    """
    if not functions:
        return lambda x: x
    
    def piped(initial):
        result = initial
        for func in functions:
            result = func(result)
        return result
    
    # Copy metadata
    func_names = [f.__name__ for f in functions if hasattr(f, '__name__')]
    piped.__name__ = f"simple_pipeline({', '.join(func_names)})"
    
    return piped


def try_chain(list fns, bint fail=False, object default_value=None):
    """
    Try functions in sequence until one succeeds.
    
    Optimized with:
    - Exception handling optimization
    - Early termination
    """
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


cpdef object deep_attribute_set(object obj, str path, object value):
    """
    Set a value in a nested object using dot notation.
    
    Optimized with:
    - Direct path parsing
    - Efficient object traversal
    """
    if "." not in path:
        return _anyset(obj, path, value)
    
    cdef str key
    cdef str rest
    
    key, rest = path.split(".", 1)
    nested_obj = _anyget(obj, key, {})
    _anyset(obj, key, nested_obj)
    return deep_attribute_set(nested_obj, rest, value)


cdef object _anyset(object obj, str key, object value):
    """Set attribute on object or dict."""
    if isinstance(obj, dict):
        obj[key] = value
    else:
        setattr(obj, key, value)
    return obj


def set_defaults(dict base=None, **kwargs):
    """
    Set default values in a dictionary.
    
    Optimized with:
    - Direct dictionary manipulation
    """
    if base is None:
        base = {}
    
    cdef str k
    cdef object v
    
    for k, v in kwargs.items():
        if k not in base:
            base[k] = v
    
    return base


cpdef dict dict_without_keys(dict d, list keys):
    """
    Return dictionary without specified keys.
    
    Optimized with:
    - Set-based key filtering
    """
    if not d:
        return {}
    
    cdef set key_set = set(keys)
    return {k: v for k, v in d.items() if k not in key_set}


# Optimized filter_nulls (duplicate from _collections_cy to avoid circular import)
cpdef object filter_nulls(object obj):
    """
    Recursively remove None values and empty containers.
    
    Optimized with:
    - Direct type checking
    - In-place filtering where possible
    - Reduced intermediate object creation
    """
    cdef dict filtered_dict
    cdef list filtered_list
    cdef object key, value, filtered_value
    
    if isinstance(obj, dict):
        filtered_dict = {}
        for key, value in obj.items():
            if value is not None:
                if isinstance(value, (dict, list)):
                    filtered_value = filter_nulls(value)
                    if filtered_value:  # Don't add empty containers
                        filtered_dict[key] = filtered_value
                else:
                    filtered_dict[key] = value
        return filtered_dict
        
    elif isinstance(obj, list):
        filtered_list = []
        for value in obj:
            if value is not None:
                if isinstance(value, (dict, list)):
                    filtered_value = filter_nulls(value)
                    if filtered_value:  # Don't add empty containers
                        filtered_list.append(filtered_value)
                else:
                    filtered_list.append(value)
        return filtered_list
    else:
        return obj