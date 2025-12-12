"""Tests for utilities._yaml module."""

import datetime

import pytest

from good_common.utilities._yaml import (
    normalize_unicode_and_newlines,
    yaml_dump,
    yaml_dumps,
    yaml_load,
    yaml_loads,
)


class TestYAMLLoading:
    """Test YAML loading functionality."""

    def test_yaml_loads_simple_dict(self):
        """Test loading simple YAML dictionary."""
        yaml_str = """
name: test
value: 123
"""
        result = yaml_loads(yaml_str)
        assert result == {"name": "test", "value": 123}

    def test_yaml_loads_nested_dict(self):
        """Test loading nested YAML structure."""
        yaml_str = """
parent:
  child:
    grandchild: value
"""
        result = yaml_loads(yaml_str)
        assert result["parent"]["child"]["grandchild"] == "value"

    def test_yaml_loads_list(self):
        """Test loading YAML list."""
        yaml_str = """
items:
  - first
  - second
  - third
"""
        result = yaml_loads(yaml_str)
        assert result["items"] == ["first", "second", "third"]

    def test_yaml_loads_mixed_types(self):
        """Test loading YAML with mixed types."""
        yaml_str = """
string: hello
integer: 42
float: 3.14
boolean: true
null_value: null
"""
        result = yaml_loads(yaml_str)
        assert result["string"] == "hello"
        assert result["integer"] == 42
        assert result["float"] == 3.14
        assert result["boolean"] is True
        assert result["null_value"] is None

    def test_yaml_load_from_file(self, tmp_path):
        """Test loading YAML from file."""
        yaml_file = tmp_path / "test.yaml"
        yaml_file.write_text("key: value\ncount: 10")
        result = yaml_load(yaml_file)
        assert result == {"key": "value", "count": 10}

    def test_yaml_load_unicode(self, tmp_path):
        """Test loading YAML with unicode characters."""
        yaml_file = tmp_path / "unicode.yaml"
        yaml_file.write_text("name: 日本語\nemoji: 🎉", encoding="utf-8")
        result = yaml_load(yaml_file)
        assert result["name"] == "日本語"
        assert result["emoji"] == "🎉"


class TestYAMLDumping:
    """Test YAML dumping functionality."""

    def test_yaml_dumps_simple_dict(self):
        """Test dumping simple dictionary to YAML."""
        data = {"name": "test", "value": 123}
        result = yaml_dumps(data)
        assert "name: test" in result
        assert "value: 123" in result

    def test_yaml_dumps_nested_dict(self):
        """Test dumping nested dictionary."""
        data = {"parent": {"child": {"grandchild": "value"}}}
        result = yaml_dumps(data)
        assert "parent:" in result
        assert "child:" in result
        assert "grandchild: value" in result

    def test_yaml_dumps_list(self):
        """Test dumping list to YAML."""
        data = {"items": ["first", "second", "third"]}
        result = yaml_dumps(data)
        assert "items:" in result
        assert "- first" in result
        assert "- second" in result

    def test_yaml_dumps_multiline_string(self):
        """Test dumping multiline string with literal style."""
        data = {"description": "Line 1\nLine 2\nLine 3"}
        result = yaml_dumps(data)
        # Should use literal style (|) for multiline strings
        assert "description: |" in result or "description: |-" in result

    def test_yaml_dumps_with_sort_keys(self):
        """Test dumping with sorted keys."""
        data = {"zebra": 1, "apple": 2, "banana": 3}
        result = yaml_dumps(data, sort_keys=True)
        lines = [line for line in result.split("\n") if line.strip()]
        # Check order
        assert lines[0].startswith("apple:")
        assert lines[1].startswith("banana:")
        assert lines[2].startswith("zebra:")

    def test_yaml_dumps_set(self):
        """Test dumping set (should be sorted list)."""
        data = {"items": {3, 1, 2}}
        result = yaml_dumps(data)
        # Set should be represented as sorted list
        assert "items:" in result
        parsed = yaml_loads(result)
        assert parsed["items"] == [1, 2, 3]

    def test_yaml_dumps_datetime(self):
        """Test dumping datetime objects."""
        dt = datetime.datetime(2024, 1, 15, 10, 30, 45)
        data = {"timestamp": dt}
        result = yaml_dumps(data)
        assert "timestamp:" in result
        assert "2024-01-15" in result

    def test_yaml_dumps_unicode(self):
        """Test dumping unicode characters."""
        data = {"name": "日本語", "emoji": "🎉"}
        result = yaml_dumps(data)
        assert "日本語" in result
        # Emoji might be escaped or preserved, both are valid
        assert ("🎉" in result or "U0001F389" in result)

    def test_yaml_dump_to_file(self, tmp_path):
        """Test dumping YAML to file."""
        yaml_file = tmp_path / "output.yaml"
        data = {"key": "value", "count": 10}
        yaml_dump(yaml_file, data)
        assert yaml_file.exists()
        content = yaml_file.read_text()
        assert "key: value" in content
        assert "count: 10" in content

    def test_yaml_dump_pathlib_path(self, tmp_path):
        """Test dumping with pathlib.Path object."""
        yaml_file = tmp_path / "pathlib.yaml"
        data = {"test": "pathlib"}
        yaml_dump(yaml_file, data)
        loaded = yaml_load(yaml_file)
        assert loaded == data

    def test_yaml_dumps_no_aliases(self):
        """Test that aliases/references are not created."""
        shared_list = [1, 2, 3]
        data = {"list1": shared_list, "list2": shared_list}
        result = yaml_dumps(data)
        # Should not contain YAML aliases (&id or *id)
        assert "&" not in result
        assert "*" not in result


class TestNormalizeUnicodeAndNewlines:
    """Test normalize_unicode_and_newlines function."""

    def test_normalize_simple_string(self):
        """Test normalizing simple string."""
        result = normalize_unicode_and_newlines("hello")
        assert result == "hello"

    def test_normalize_escaped_unicode(self):
        """Test normalizing escaped unicode sequences."""
        result = normalize_unicode_and_newlines("hello \\u0041 world")
        assert result == "hello A world"

    def test_normalize_escaped_newlines(self):
        """Test normalizing escaped newlines."""
        result = normalize_unicode_and_newlines("line1\\nline2")
        assert result == "line1\nline2"

    def test_normalize_dict(self):
        """Test normalizing dictionary."""
        data = {"key": "value\\nwith\\nnewlines", "unicode": "\\u0041BC"}
        result = normalize_unicode_and_newlines(data)
        assert result["key"] == "value\nwith\nnewlines"
        assert result["unicode"] == "ABC"

    def test_normalize_nested_dict(self):
        """Test normalizing nested dictionary."""
        data = {"parent": {"child": "\\u0048ello\\nWorld"}}
        result = normalize_unicode_and_newlines(data)
        assert result["parent"]["child"] == "Hello\nWorld"

    def test_normalize_list(self):
        """Test normalizing list."""
        data = ["item\\n1", "item\\u0032", "item3"]
        result = normalize_unicode_and_newlines(data)
        assert result == ["item\n1", "item2", "item3"]

    def test_normalize_mixed_structure(self):
        """Test normalizing complex mixed structure."""
        data = {
            "strings": ["hello\\nworld", "test\\u0041"],
            "nested": {"value": "data\\u0042"},
        }
        result = normalize_unicode_and_newlines(data)
        assert result["strings"] == ["hello\nworld", "testA"]
        assert result["nested"]["value"] == "dataB"

    def test_normalize_non_string_types(self):
        """Test that non-string types are preserved."""
        data = {"int": 42, "float": 3.14, "bool": True, "none": None}
        result = normalize_unicode_and_newlines(data)
        assert result == data

    def test_normalize_empty_structures(self):
        """Test normalizing empty structures."""
        assert normalize_unicode_and_newlines({}) == {}
        assert normalize_unicode_and_newlines([]) == []
        assert normalize_unicode_and_newlines("") == ""


class TestYAMLRoundTrip:
    """Test round-trip serialization and deserialization."""

    def test_roundtrip_simple_dict(self):
        """Test round-trip with simple dictionary."""
        original = {"name": "test", "value": 123, "flag": True}
        yaml_str = yaml_dumps(original)
        result = yaml_loads(yaml_str)
        assert result == original

    def test_roundtrip_nested_structure(self):
        """Test round-trip with nested structure."""
        original = {
            "level1": {
                "level2": {"level3": "deep", "list": [1, 2, 3]},
                "another": "value",
            }
        }
        yaml_str = yaml_dumps(original)
        result = yaml_loads(yaml_str)
        assert result == original

    def test_roundtrip_with_file(self, tmp_path):
        """Test round-trip through file."""
        yaml_file = tmp_path / "roundtrip.yaml"
        original = {"data": {"nested": [1, 2, 3]}, "string": "test"}
        yaml_dump(yaml_file, original)
        result = yaml_load(yaml_file)
        assert result == original

    def test_roundtrip_unicode(self, tmp_path):
        """Test round-trip with unicode."""
        yaml_file = tmp_path / "unicode_roundtrip.yaml"
        original = {"japanese": "日本語", "emoji": "🎉🎊"}
        yaml_dump(yaml_file, original)
        result = yaml_load(yaml_file)
        assert result == original

    def test_roundtrip_multiline(self, tmp_path):
        """Test round-trip with multiline strings."""
        yaml_file = tmp_path / "multiline.yaml"
        original = {"text": "Line 1\nLine 2\nLine 3"}
        yaml_dump(yaml_file, original)
        result = yaml_load(yaml_file)
        assert result == original

    def test_roundtrip_set_becomes_list(self):
        """Test that sets become sorted lists."""
        original = {"items": {3, 1, 2}}
        yaml_str = yaml_dumps(original)
        result = yaml_loads(yaml_str)
        # Set is converted to sorted list
        assert result["items"] == [1, 2, 3]


class TestYAMLEdgeCases:
    """Test edge cases and special scenarios."""

    def test_empty_yaml(self):
        """Test with empty YAML."""
        result = yaml_loads("")
        assert result is None

    def test_yaml_with_comments_preserved_on_load(self, tmp_path):
        """Test that YAML can be loaded even with comments."""
        yaml_file = tmp_path / "comments.yaml"
        yaml_file.write_text("# Comment\nkey: value  # inline comment\n")
        result = yaml_load(yaml_file)
        assert result == {"key": "value"}

    def test_special_characters(self):
        """Test with special characters."""
        data = {"special": "!@#$%^&*()[]{}|\\:;'\"<>?,./"}
        yaml_str = yaml_dumps(data)
        result = yaml_loads(yaml_str)
        assert result == data

    def test_very_nested_structure(self):
        """Test deeply nested structure."""
        data = {"l1": {"l2": {"l3": {"l4": {"l5": {"l6": "deep"}}}}}}
        yaml_str = yaml_dumps(data)
        result = yaml_loads(yaml_str)
        assert result == data

    def test_large_list(self):
        """Test with large list."""
        data = {"numbers": list(range(100))}
        yaml_str = yaml_dumps(data)
        result = yaml_loads(yaml_str)
        assert result == data

    def test_mixed_list_types(self):
        """Test list with mixed types."""
        data = {"mixed": [1, "string", True, None, 3.14]}
        yaml_str = yaml_dumps(data)
        result = yaml_loads(yaml_str)
        assert result == data

    def test_yaml_dumps_custom_kwargs(self):
        """Test yaml_dumps with custom kwargs."""
        data = {"test": "value"}
        result = yaml_dumps(data, width=50, indent=4)
        assert "test:" in result

    def test_yaml_dump_custom_kwargs(self, tmp_path):
        """Test yaml_dump with custom kwargs."""
        yaml_file = tmp_path / "custom.yaml"
        data = {"test": "value"}
        yaml_dump(yaml_file, data, width=50, indent=4)
        assert yaml_file.exists()


class TestYAMLWithURL:
    """Test YAML with URL type (if available)."""

    def test_yaml_dumps_with_url(self):
        """Test dumping URL objects."""
        try:
            from good_common.types import URL

            url = URL("https://example.com")
            data = {"url": url}
            result = yaml_dumps(data)
            assert "https://example.com" in result
        except ImportError:
            pytest.skip("URL type not available")

    def test_yaml_roundtrip_with_url(self, tmp_path):
        """Test round-trip with URL objects."""
        try:
            from good_common.types import URL

            yaml_file = tmp_path / "url.yaml"
            url = URL("https://example.com/path")
            data = {"website": url}
            yaml_dump(yaml_file, data)
            result = yaml_load(yaml_file)
            # URL becomes string in YAML
            assert result["website"] == "https://example.com/path"
        except ImportError:
            pytest.skip("URL type not available")
