"""
Import wrapper for Cython-optimized functions with fallbacks to pure Python.

This module attempts to import Cython-optimized versions of utility functions,
falling back to pure Python implementations if Cython modules are not available.
"""

from typing import Dict

# Track what's available
CYTHON_AVAILABLE = {"collections": False, "functional": False, "strings": False}

# Try to import Cython collections
try:
    from ._collections_cy import (
        sort_object_keys as sort_object_keys_cy,
        index_object as index_object_cy,
        deindex_object as deindex_object_cy,
        filter_nulls as filter_nulls_cy,
        merge_dicts as merge_dicts_cy,
        deduplicate_dicts_cy,
        flatten_list as flatten_list_cy,
        recursive_get as recursive_get_cy,
        path_tuple_to_string as path_tuple_to_string_cy,
        path_string_to_tuple as path_string_to_tuple_cy,
    )

    CYTHON_AVAILABLE["collections"] = True

    # Use Cython versions
    sort_object_keys = sort_object_keys_cy
    index_object = index_object_cy
    deindex_object = deindex_object_cy
    merge_dicts = merge_dicts_cy
    deduplicate_dicts = deduplicate_dicts_cy
    flatten_list = flatten_list_cy
    recursive_get = recursive_get_cy
    path_tuple_to_string = path_tuple_to_string_cy
    path_string_to_tuple = path_string_to_tuple_cy

except ImportError:
    # Fall back to pure Python
    from ._collections import (
        sort_object_keys,
        index_object,
        deindex_object,
        merge_dicts,
        deduplicate_dicts,
        flatten_list,
        recursive_get,
        path_tuple_to_string,
        path_string_to_tuple,
    )

    deduplicate_dicts_cy = deduplicate_dicts  # Alias for compatibility

# Try to import Cython functional utilities
try:
    from ._functional_cy import (
        filter_nulls as filter_nulls_cy_func,
        deep_attribute_get as deep_attribute_get_cy,
        simple_pipeline as simple_pipeline_cy,
        try_chain as try_chain_cy,
        deep_attribute_set as deep_attribute_set_cy,
        set_defaults as set_defaults_cy,
        dict_without_keys as dict_without_keys_cy,
    )

    CYTHON_AVAILABLE["functional"] = True

    # Use Cython versions (filter_nulls already imported from collections)
    if not CYTHON_AVAILABLE["collections"]:
        filter_nulls = filter_nulls_cy_func
    else:
        filter_nulls = filter_nulls_cy

    deep_attribute_get = deep_attribute_get_cy
    simple_pipeline = simple_pipeline_cy
    try_chain = try_chain_cy
    deep_attribute_set = deep_attribute_set_cy
    set_defaults = set_defaults_cy
    dict_without_keys = dict_without_keys_cy

except ImportError:
    # Fall back to pure Python
    from ._functional import (
        filter_nulls,
        deep_attribute_get,
        simple_pipeline,
        try_chain,
        deep_attribute_set,
        set_defaults,
        dict_without_keys,
    )

# Try to import Cython string utilities
try:
    from ._strings_cy import (
        camel_to_snake as camel_to_snake_cy,
        snake_to_camel as snake_to_camel_cy,
        camel_to_kebab as camel_to_kebab_cy,
        snake_to_kebab as snake_to_kebab_cy,
        kebab_to_snake as kebab_to_snake_cy,
        kebab_to_camel as kebab_to_camel_cy,
        is_uuid as is_uuid_cy,
        detect_string_type as detect_string_type_cy,
        encode_base32 as encode_base32_cy,
        camel_to_slug as camel_to_slug_cy,
        slug_to_camel as slug_to_camel_cy,
        slug_to_snake as slug_to_snake_cy,
        slug_to_kebab as slug_to_kebab_cy,
    )

    CYTHON_AVAILABLE["strings"] = True

    # Use Cython versions
    camel_to_snake = camel_to_snake_cy
    snake_to_camel = snake_to_camel_cy
    camel_to_kebab = camel_to_kebab_cy
    snake_to_kebab = snake_to_kebab_cy
    kebab_to_snake = kebab_to_snake_cy
    kebab_to_camel = kebab_to_camel_cy
    is_uuid = is_uuid_cy
    detect_string_type = detect_string_type_cy
    encode_base32 = encode_base32_cy
    camel_to_slug = camel_to_slug_cy
    slug_to_camel = slug_to_camel_cy
    slug_to_snake = slug_to_snake_cy
    slug_to_kebab = slug_to_kebab_cy

except ImportError:
    # Fall back to pure Python
    from ._strings import (
        camel_to_snake,
        snake_to_camel,
        camel_to_kebab,
        snake_to_kebab,
        kebab_to_snake,
        kebab_to_camel,
        is_uuid,
        detect_string_type,
        encode_base32,
        camel_to_slug,
        slug_to_camel,
        slug_to_snake,
        slug_to_kebab,
    )


def get_optimization_status() -> Dict[str, bool]:
    """
    Get the status of Cython optimizations.

    Returns:
        Dictionary mapping module names to their Cython availability status.
    """
    return CYTHON_AVAILABLE.copy()


def is_optimized() -> bool:
    """
    Check if any Cython optimizations are available.

    Returns:
        True if at least one Cython module is available, False otherwise.
    """
    return any(CYTHON_AVAILABLE.values())


# Export all functions
__all__ = [
    # Collections
    "sort_object_keys",
    "index_object",
    "deindex_object",
    "merge_dicts",
    "deduplicate_dicts",
    "deduplicate_dicts_cy",
    "flatten_list",
    "recursive_get",
    "path_tuple_to_string",
    "path_string_to_tuple",
    # Functional
    "filter_nulls",
    "deep_attribute_get",
    "simple_pipeline",
    "try_chain",
    "deep_attribute_set",
    "set_defaults",
    "dict_without_keys",
    # Strings
    "camel_to_snake",
    "snake_to_camel",
    "camel_to_kebab",
    "snake_to_kebab",
    "kebab_to_snake",
    "kebab_to_camel",
    "is_uuid",
    "detect_string_type",
    "encode_base32",
    "camel_to_slug",
    "slug_to_camel",
    "slug_to_snake",
    "slug_to_kebab",
    # Status functions
    "get_optimization_status",
    "is_optimized",
]
