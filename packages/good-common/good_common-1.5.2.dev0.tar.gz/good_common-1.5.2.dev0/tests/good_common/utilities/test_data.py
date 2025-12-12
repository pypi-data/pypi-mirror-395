"""Tests for utilities._data module."""

import pytest
from pydantic import BaseModel

from good_common.utilities._data import (
    b64_decode,
    b64_encode,
    farmhash_bytes,
    farmhash_hex,
    farmhash_string,
    int_to_base62,
    is_int,
    serialize_any,
    signed_64_to_unsigned_128,
    to_float,
    to_int,
    to_numeric,
)


class TestIntConversion:
    """Test integer conversion functions."""

    def test_is_int_valid_integer(self):
        """Test is_int with valid integers."""
        assert is_int("123")
        assert is_int("0")
        assert is_int("-456")
        assert is_int(789)

    def test_is_int_invalid(self):
        """Test is_int with invalid values."""
        assert not is_int("abc")
        assert not is_int("12.34")
        assert not is_int(None)
        assert not is_int("")
        assert not is_int("12a")

    def test_to_int_valid(self):
        """Test to_int with valid values."""
        assert to_int("123") == 123
        assert to_int("0") == 0
        assert to_int("-456") == -456
        assert to_int(789) == 789
        assert to_int(12.9) == 12

    def test_to_int_invalid(self):
        """Test to_int with invalid values returns None."""
        assert to_int("abc") is None
        assert to_int(None) is None
        assert to_int("") is None
        assert to_int("12.34a") is None


class TestFloatConversion:
    """Test float conversion functions."""

    def test_to_float_valid(self):
        """Test to_float with valid values."""
        assert to_float("12.34") == 12.34
        assert to_float("0") == 0.0
        assert to_float("-45.67") == -45.67
        assert to_float(89) == 89.0
        assert to_float(12.5) == 12.5

    def test_to_float_invalid(self):
        """Test to_float with invalid values returns None."""
        assert to_float("abc") is None
        assert to_float(None) is None
        assert to_float("") is None
        assert to_float("12.34.56") is None


class TestNumericConversion:
    """Test to_numeric function."""

    def test_to_numeric_integer(self):
        """Test to_numeric returns int when possible."""
        assert to_numeric("123") == 123
        assert to_numeric("0") == 0
        assert to_numeric("-456") == -456
        assert isinstance(to_numeric("123"), int)

    def test_to_numeric_float(self):
        """Test to_numeric returns float when needed."""
        assert to_numeric("12.34") == 12.34
        assert to_numeric("0.5") == 0.5
        assert to_numeric("-45.67") == -45.67
        assert isinstance(to_numeric("12.34"), float)

    def test_to_numeric_invalid(self):
        """Test to_numeric with invalid values returns None."""
        assert to_numeric("abc") is None
        assert to_numeric("") is None
        # Note: to_numeric doesn't handle None gracefully - it raises TypeError


class TestBase62Conversion:
    """Test base62 conversion functions."""

    def test_signed_64_to_unsigned_128_positive(self):
        """Test conversion of positive numbers."""
        assert signed_64_to_unsigned_128(100) == 100
        assert signed_64_to_unsigned_128(0) == 0

    def test_signed_64_to_unsigned_128_negative(self):
        """Test conversion of negative numbers."""
        result = signed_64_to_unsigned_128(-1)
        assert result == (1 << 64) - 1
        result = signed_64_to_unsigned_128(-100)
        assert result == (1 << 64) - 100

    def test_int_to_base62_zero(self):
        """Test base62 conversion of zero."""
        assert int_to_base62(0) == "0"

    def test_int_to_base62_positive(self):
        """Test base62 conversion of positive numbers."""
        result = int_to_base62(62)
        assert isinstance(result, str)
        assert len(result) > 0
        # 62 in base62 should be "10"
        assert result == "10"

    def test_int_to_base62_negative(self):
        """Test base62 conversion of negative numbers."""
        result = int_to_base62(-1)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_int_to_base62_large_number(self):
        """Test base62 conversion of large numbers."""
        result = int_to_base62(1000000)
        assert isinstance(result, str)
        assert len(result) > 0


class TestFarmhash:
    """Test farmhash functions."""

    def test_farmhash_string_basic(self):
        """Test basic farmhash_string functionality."""
        result = farmhash_string("test")
        assert isinstance(result, str)
        assert len(result) > 0

    def test_farmhash_string_deterministic(self):
        """Test that farmhash_string is deterministic."""
        result1 = farmhash_string("test")
        result2 = farmhash_string("test")
        assert result1 == result2

    def test_farmhash_string_different_inputs(self):
        """Test that different inputs produce different hashes."""
        result1 = farmhash_string("test1")
        result2 = farmhash_string("test2")
        assert result1 != result2

    def test_farmhash_string_no_base62(self):
        """Test farmhash_string without base62 (default)."""
        result = farmhash_string("test", to_base62=False)
        assert isinstance(result, str)
        assert len(result) > 0
        # Default uses encode_base32 which returns a string

    def test_farmhash_bytes(self):
        """Test farmhash_bytes returns bytes."""
        result = farmhash_bytes("test")
        assert isinstance(result, bytes)
        assert len(result) == 8  # 64-bit hash = 8 bytes

    def test_farmhash_bytes_deterministic(self):
        """Test that farmhash_bytes is deterministic."""
        result1 = farmhash_bytes("test")
        result2 = farmhash_bytes("test")
        assert result1 == result2

    def test_farmhash_hex(self):
        """Test farmhash_hex returns hex string."""
        result = farmhash_hex("test")
        assert isinstance(result, str)
        assert len(result) == 16  # 8 bytes = 16 hex chars
        # Verify it's valid hex
        int(result, 16)

    def test_farmhash_hex_deterministic(self):
        """Test that farmhash_hex is deterministic."""
        result1 = farmhash_hex("test")
        result2 = farmhash_hex("test")
        assert result1 == result2


class TestBase64Encoding:
    """Test base64 encoding/decoding functions."""

    def test_b64_encode_string(self):
        """Test encoding a string to base64."""
        result = b64_encode("hello")
        assert isinstance(result, str)
        assert result == "aGVsbG8="

    def test_b64_encode_non_string(self):
        """Test encoding non-string values."""
        result = b64_encode(123)
        assert isinstance(result, str)
        # Should convert to string first
        assert result == b64_encode("123")

    def test_b64_decode_valid(self):
        """Test decoding valid base64 string."""
        encoded = "aGVsbG8="
        result = b64_decode(encoded)
        assert result == "hello"

    def test_b64_decode_invalid(self):
        """Test decoding invalid base64 returns original."""
        result = b64_decode("not base64")
        assert result == "not base64"

    def test_b64_decode_non_string(self):
        """Test decoding non-string values."""
        result = b64_decode(123)
        assert result == "123"

    def test_b64_roundtrip(self):
        """Test encoding and decoding roundtrip."""
        original = "test data with special chars: !@#$%"
        encoded = b64_encode(original)
        decoded = b64_decode(encoded)
        assert decoded == original

    def test_b64_encode_unicode(self):
        """Test encoding unicode strings."""
        result = b64_encode("日本語")
        assert isinstance(result, str)
        decoded = b64_decode(result)
        assert decoded == "日本語"

    def test_b64_encode_empty_string(self):
        """Test encoding empty string."""
        result = b64_encode("")
        assert isinstance(result, str)
        decoded = b64_decode(result)
        assert decoded == ""


class TestSerializeAny:
    """Test serialize_any function."""

    def test_serialize_dict(self):
        """Test serializing dictionary."""
        data = {"key": "value", "num": 123}
        result = serialize_any(data)
        assert isinstance(result, str)
        assert "key" in result
        assert "value" in result

    def test_serialize_list(self):
        """Test serializing list."""
        data = [1, 2, 3, "test"]
        result = serialize_any(data)
        assert isinstance(result, str)
        assert "1" in result
        assert "test" in result

    def test_serialize_tuple(self):
        """Test serializing tuple."""
        data = (1, 2, 3)
        result = serialize_any(data)
        assert isinstance(result, str)

    def test_serialize_string(self):
        """Test serializing string."""
        result = serialize_any("test")
        assert result == "test"

    def test_serialize_int(self):
        """Test serializing integer."""
        result = serialize_any(123)
        assert result == "123"

    def test_serialize_float(self):
        """Test serializing float."""
        result = serialize_any(12.34)
        assert result == "12.34"

    def test_serialize_pydantic_model(self):
        """Test serializing Pydantic model."""

        class TestModel(BaseModel):
            name: str
            value: int

        model = TestModel(name="test", value=123)
        result = serialize_any(model)
        assert isinstance(result, str)
        assert "test" in result
        assert "123" in result

    def test_serialize_pydantic_excludes_none(self):
        """Test that None values are excluded from Pydantic serialization."""

        class TestModel(BaseModel):
            name: str
            optional: str | None = None

        model = TestModel(name="test")
        result = serialize_any(model)
        assert "optional" not in result

    def test_serialize_nested_dict(self):
        """Test serializing nested dictionary."""
        data = {"outer": {"inner": {"deep": "value"}}}
        result = serialize_any(data)
        assert isinstance(result, str)
        assert "deep" in result

    def test_serialize_unsupported_type(self):
        """Test that unsupported types raise ValueError."""

        class CustomClass:
            pass

        with pytest.raises(ValueError, match="Cannot serialize"):
            serialize_any(CustomClass())

    def test_serialize_dict_sorted_keys(self):
        """Test that dict keys are sorted in serialization."""
        data = {"zebra": 1, "apple": 2, "banana": 3}
        result = serialize_any(data)
        # Keys should be sorted
        assert result.index("apple") < result.index("banana")
        assert result.index("banana") < result.index("zebra")


class TestEdgeCases:
    """Test edge cases and special scenarios."""

    def test_farmhash_empty_string(self):
        """Test farmhash with empty string."""
        result = farmhash_string("")
        assert isinstance(result, str)

    def test_farmhash_unicode(self):
        """Test farmhash with unicode."""
        result = farmhash_string("日本語🎉")
        assert isinstance(result, str)

    def test_base62_boundary_values(self):
        """Test base62 conversion at boundary values."""
        assert int_to_base62(0) == "0"
        assert int_to_base62(1) == "1"
        assert int_to_base62(61) == "z"
        assert int_to_base62(62) == "10"

    def test_numeric_conversion_edge_cases(self):
        """Test numeric conversion with edge cases."""
        assert to_numeric("0") == 0
        assert to_numeric("0.0") == 0.0
        assert to_numeric("-0") == 0

    def test_serialize_empty_collections(self):
        """Test serializing empty collections."""
        assert serialize_any({}) == "{}"
        assert serialize_any([]) == "[]"

    def test_b64_special_characters(self):
        """Test base64 with special characters."""
        special = "!@#$%^&*()[]{}|\\:;'\"<>?,./`~"
        encoded = b64_encode(special)
        decoded = b64_decode(encoded)
        assert decoded == special
