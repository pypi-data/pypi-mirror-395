import pytest
from good_common.utilities import (
    try_chain,
    deep_attribute_get,
    deep_attribute_set,
    set_defaults,
    filter_nulls,
    object_farmhash_base62,
)


# Test for try_chain
def test_try_chain():
    def fail_func():
        raise ValueError("Failed")

    def success_func(x):
        return x * 2

    chain = try_chain([fail_func, success_func])
    assert chain(5) == 10

    fail_chain = try_chain([fail_func, fail_func], fail=True)
    with pytest.raises(ValueError):
        fail_chain(5)

    default_chain = try_chain([fail_func, fail_func], default_value="default")
    assert default_chain(5) == "default"


# Tests for deep_attribute_get
def test_deep_attribute_get():
    obj = {
        "a": {"b": [{"c": 1}, {"c": 2}], "d": {"e": "value"}},
        "f": [1, 2, 3],
        "g": {"h": [{"i": "test"}]},
    }

    assert deep_attribute_get(obj, "a.b[0].c") == 1
    # assert deep_attribute_get(obj, "a.b[*].c") == [1, 2] NOT SUPPORTED
    assert deep_attribute_get(obj, "a.d.e") == "value"
    assert deep_attribute_get(obj, "f[1]") == 2
    assert deep_attribute_get(obj, "g.h[0].i") == "test"
    assert deep_attribute_get(obj, "nonexistent", default="not found") == "not found"

    result = deep_attribute_get(obj, "a.b[*].c", return_paths=True)
    assert result == [(1, "a.b[0].c"), (2, "a.b[1].c")]


# Test for deep_attribute_set
def test_deep_attribute_set():
    obj = {"a": {"b": {"c": 1}}}
    deep_attribute_set(obj, "a.b.c", 2)
    assert obj["a"]["b"]["c"] == 2

    deep_attribute_set(obj, "a.b.d", 3)
    assert obj["a"]["b"]["d"] == 3

    # deep_attribute_set(obj, "x.y.z", 4) NOT SUPPORTED
    # assert obj["x"]["y"]["z"] == 4


# Test for set_defaults
# def test_set_defaults():
#     base = {"a": 1, "b": None}
#     result = set_defaults(base, b=2, c=3)
#     assert result == {"a": 1, "b": 2, "c": 3}

#     result = set_defaults(b=2, c=3)
#     assert result == {"b": 2, "c": 3}


# Test for filter_nulls
def test_filter_nulls():
    obj = {
        "a": 1,
        "b": None,
        "c": {"d": 2, "e": None, "f": [1, None, 3]},
        "g": [{"h": 4, "i": None}, {"j": None}, {"k": 5}],
    }

    result = filter_nulls(obj)
    assert result == {"a": 1, "c": {"d": 2, "f": [1, 3]}, "g": [{"h": 4}, {"k": 5}]}


# Additional tests for edge cases and specific behaviors


def test_deep_attribute_get_with_nonexistent_path():
    obj = {"a": {"b": 1}}
    assert deep_attribute_get(obj, "a.c.d", default="not found") == "not found"


def test_try_chain_with_mixed_functions():
    def int_func(x):
        return int(x)

    def float_func(x):
        return float(x)

    def str_func(x):
        return str(x)

    chain = try_chain([int_func, float_func, str_func])
    assert chain("10") == 10
    assert chain("10.5") == 10.5
    assert chain("abc") == "abc"


def test_set_defaults_with_falsy_values():
    base = {"a": 0, "b": ""}
    result = set_defaults(base, a=1, b="test", c=False)
    assert result == {"a": 0, "b": "", "c": False}


def test_filter_nulls_with_empty_containers():
    obj = {"a": [], "b": {}, "c": [None], "d": {"e": None}}
    result = filter_nulls(obj)
    assert result == {}


def test_simple_pipeline():
    """Test simple_pipeline function composition."""
    from good_common.utilities import simple_pipeline
    
    # Test empty pipeline
    identity = simple_pipeline()
    assert identity(42) == 42
    
    # Test single function
    double = simple_pipeline(lambda x: x * 2)
    assert double(5) == 10
    
    # Test multiple functions
    process = simple_pipeline(
        lambda x: x * 2,
        lambda x: x + 1,
        lambda x: str(x)
    )
    assert process(5) == "11"
    
    # Test with named functions
    def add_one(x): return x + 1
    def multiply_two(x): return x * 2
    pipeline = simple_pipeline(add_one, multiply_two)
    assert pipeline(5) == 12
    assert "add_one" in pipeline.__name__
    assert "multiply_two" in pipeline.__name__


def test_try_chain_error_cases():
    """Test try_chain with various error scenarios."""
    # Test fail=True raises error after all functions fail
    def always_fail(x):
        raise ValueError("fail")
    
    chain = try_chain([always_fail], fail=True)
    with pytest.raises(ValueError, match="Could not process"):
        chain(10)
    
    # Test default_value is returned when all fail and fail=False
    chain = try_chain([always_fail], fail=False, default_value="fallback")
    assert chain(10) == "fallback"


def test_deep_attribute_get_with_wildcard():
    """Test deep_attribute_get with wildcard patterns and edge cases."""
    obj = {
        "items": [
            {"name": "a", "value": 1},
            {"name": "b", "value": 2},
            {"name": "c", "value": 3}
        ]
    }
    
    # Test wildcard in list with return_paths
    result = deep_attribute_get(obj, "items[*].value", return_paths=True)
    assert result == [(1, "items[0].value"), (2, "items[1].value"), (3, "items[2].value")]
    
    # Test wildcard in dict with return_paths
    obj2 = {"a": {"x": 1}, "b": {"x": 2}, "c": {"x": 3}}
    result = deep_attribute_get(obj2, "*.x", return_paths=True)
    assert len(result) == 3
    
    # Test wildcard with non-iterable (should return default)
    obj3 = {"value": 42}
    result = deep_attribute_get(obj3, "value.*.x", default="not_found", debug=True)
    assert result == "not_found"


def test_object_farmhash_base62():
    """Test object_farmhash_base62 encoding."""
    # Test basic encoding
    result1 = object_farmhash_base62({"key": "value"})
    assert isinstance(result1, str)
    assert len(result1) > 0
    
    # Test consistent hashing
    result2 = object_farmhash_base62({"key": "value"})
    assert result1 == result2
    
    # Test different objects produce different hashes
    result3 = object_farmhash_base62({"key": "different"})
    assert result1 != result3
