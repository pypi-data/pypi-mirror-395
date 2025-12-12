from unittest.mock import Mock

# Assuming the placeholder class is in a file named placeholder.py
from good_common.types.placeholder import placeholder

def test_placeholder_init():
    ph = placeholder("test_key", default="default_value")
    assert ph.key == "test_key"
    assert ph.default == "default_value"
    assert ph.post_process is None
    assert ph.kwargs == {}

def test_placeholder_call_with_value():
    ph = placeholder("test_key")
    result = ph(test_key="value")
    assert result == "value"

def test_placeholder_call_with_default():
    ph = placeholder("test_key", default="default_value")
    result = ph(other_key="value")
    assert result == "default_value"

def test_placeholder_call_with_callable():
    mock_callable = Mock(return_value="callable_result")
    ph = placeholder("test_key", default=mock_callable)
    result = ph()
    assert result == "callable_result"
    mock_callable.assert_called_once_with()

def test_placeholder_call_with_post_process():
    def post_process(val):
        return f"processed_{val}"
    
    ph = placeholder("test_key", post_process=post_process)
    result = ph(test_key="value")
    assert result == "processed_value"

def test_placeholder_repr():
    ph = placeholder("test_key", default="default_value")
    assert repr(ph) == "{test_key[undefined]: default_value}"

def test_placeholder_repr_with_type():
    ph = placeholder[int]("test_key", default=0)
    assert repr(ph) == "{test_key[int]: 0}"

def test_placeholder_resolve_simple():
    data = {
        "key1": placeholder("test_key1"),
        "key2": "static_value"
    }
    resolved = placeholder.resolve(data, test_key1="resolved_value")
    assert resolved == {
        "key1": "resolved_value",
        "key2": "static_value"
    }

def test_placeholder_resolve_nested():
    data = {
        "outer": {
            "inner": placeholder("test_key"),
            "static": "static_value"
        },
        "list": [
            {"item": placeholder("list_key")},
            "static_item"
        ]
    }
    resolved = placeholder.resolve(data, test_key="inner_value", list_key="list_value")
    assert resolved == {
        "outer": {
            "inner": "inner_value",
            "static": "static_value"
        },
        "list": [
            {"item": "list_value"},
            "static_item"
        ]
    }

def test_placeholder_resolve_with_callable():
    mock_callable = Mock(return_value="callable_result")
    data = {
        "key": placeholder("test_key", default=mock_callable)
    }
    resolved = placeholder.resolve(data)
    assert resolved == {"key": "callable_result"}
    mock_callable.assert_called_once_with()

# Add more tests as needed to cover edge cases and additional functionality