"""Tests for utilities._binary module (Z85 encoding/decoding)."""

import pytest

from good_common.utilities._binary import Z85DecodeError, z85decode, z85encode


class TestZ85Encoding:
    """Test Z85 encoding functionality."""

    def test_z85encode_basic(self):
        """Test basic Z85 encoding."""
        data = b"hello"
        encoded = z85encode(data)
        assert isinstance(encoded, bytes)
        assert len(encoded) > 0

    def test_z85encode_empty_bytes(self):
        """Test encoding empty bytes."""
        encoded = z85encode(b"")
        assert encoded == b""

    def test_z85encode_all_zeros(self):
        """Test encoding all zero bytes."""
        data = b"\x00\x00\x00\x00"
        encoded = z85encode(data)
        assert isinstance(encoded, bytes)
        # All zeros should encode to '00000'
        assert encoded == b"00000"

    def test_z85encode_single_byte(self):
        """Test encoding a single byte."""
        data = b"\x01"
        encoded = z85encode(data)
        assert isinstance(encoded, bytes)
        assert len(encoded) > 0

    def test_z85encode_with_padding(self):
        """Test encoding with various padding requirements."""
        # Different lengths to test padding logic
        for length in [1, 2, 3, 5, 6, 7]:
            data = b"x" * length
            encoded = z85encode(data)
            assert isinstance(encoded, bytes)

    def test_z85encode_various_byte_values(self):
        """Test encoding various byte values."""
        data = bytes(range(256))
        encoded = z85encode(data)
        assert isinstance(encoded, bytes)
        assert len(encoded) > 0


class TestZ85Decoding:
    """Test Z85 decoding functionality."""

    def test_z85decode_basic(self):
        """Test basic Z85 decoding."""
        # First encode, then decode
        original = b"test data"
        encoded = z85encode(original)
        decoded = z85decode(encoded)
        assert decoded == original

    def test_z85decode_empty_bytes(self):
        """Test decoding empty bytes."""
        decoded = z85decode(b"")
        assert decoded == b""

    def test_z85decode_all_zeros(self):
        """Test decoding all zeros."""
        encoded = b"00000"
        decoded = z85decode(encoded)
        assert decoded == b"\x00\x00\x00\x00"

    def test_z85decode_with_whitespace(self):
        """Test decoding with whitespace (should be ignored)."""
        original = b"hello world"
        encoded = z85encode(original)
        # Add some whitespace
        encoded_with_ws = b" ".join([encoded[i : i + 5] for i in range(0, len(encoded), 5)])
        decoded = z85decode(encoded_with_ws)
        assert decoded == original

    def test_z85decode_with_newlines(self):
        """Test decoding with newlines (should be ignored)."""
        original = b"multiline data"
        encoded = z85encode(original)
        # Add newlines
        encoded_with_newlines = encoded[:10] + b"\n" + encoded[10:]
        decoded = z85decode(encoded_with_newlines)
        assert decoded == original

    def test_z85decode_invalid_character_raises(self):
        """Test that invalid characters raise Z85DecodeError."""
        # Use a character not in the Z85 alphabet
        invalid_encoded = b"hello\x00world"  # null byte is invalid
        with pytest.raises(Z85DecodeError, match="Invalid byte code"):
            z85decode(invalid_encoded)

    def test_z85decode_truncated_input(self):
        """Test decoding with truncated input."""
        # Encode something, then truncate
        original = b"test"
        encoded = z85encode(original)
        # Truncate to non-multiple of 5
        truncated = encoded[:-1]
        # Should still decode without error (handles partial chunks)
        decoded = z85decode(truncated)
        assert isinstance(decoded, bytes)


class TestZ85RoundTrip:
    """Test round-trip encoding and decoding."""

    def test_roundtrip_simple_string(self):
        """Test round-trip with a simple string."""
        original = b"The quick brown fox"
        encoded = z85encode(original)
        decoded = z85decode(encoded)
        assert decoded == original

    def test_roundtrip_binary_data(self):
        """Test round-trip with binary data."""
        original = bytes([0, 1, 2, 3, 255, 254, 253, 128, 127])
        encoded = z85encode(original)
        decoded = z85decode(encoded)
        assert decoded == original

    def test_roundtrip_various_sizes(self):
        """Test round-trip with various data sizes."""
        for size in [1, 2, 3, 4, 5, 8, 15, 16, 31, 32, 63, 64, 127, 128, 255, 256]:
            original = bytes([(i * 7) % 256 for i in range(size)])
            encoded = z85encode(original)
            decoded = z85decode(encoded)
            assert decoded == original, f"Failed for size {size}"

    def test_roundtrip_all_byte_values(self):
        """Test round-trip with all possible byte values."""
        original = bytes(range(256))
        encoded = z85encode(original)
        decoded = z85decode(encoded)
        assert decoded == original

    def test_roundtrip_repeated_patterns(self):
        """Test round-trip with repeated patterns."""
        original = b"abcd" * 100
        encoded = z85encode(original)
        decoded = z85decode(encoded)
        assert decoded == original


class TestZ85EdgeCases:
    """Test edge cases and special scenarios."""

    def test_encode_large_data(self):
        """Test encoding large data."""
        # 10KB of data
        large_data = b"x" * 10000
        encoded = z85encode(large_data)
        decoded = z85decode(encoded)
        assert decoded == large_data

    def test_encode_alternating_zeros_ones(self):
        """Test encoding alternating zero and one bytes."""
        data = bytes([0, 255] * 50)
        encoded = z85encode(data)
        decoded = z85decode(encoded)
        assert decoded == data

    def test_encode_sequential_bytes(self):
        """Test encoding sequential byte values."""
        data = bytes(range(100))
        encoded = z85encode(data)
        decoded = z85decode(encoded)
        assert decoded == data

    def test_decode_only_valid_z85_chars(self):
        """Test that valid Z85 characters decode successfully."""
        # Use only characters from the Z85 alphabet
        valid_chars = b"0123456789ab"  # All valid Z85 chars
        # Pad to multiple of 5
        valid_chars = valid_chars + b"cde"
        decoded = z85decode(valid_chars)
        assert isinstance(decoded, bytes)

    def test_encode_decode_preserves_length_relationship(self):
        """Test that encoding/decoding maintains expected length relationship."""
        for length in [4, 8, 12, 16, 20]:
            data = b"x" * length
            encoded = z85encode(data)
            # Z85 encodes 4 bytes to 5 characters
            expected_encoded_len = (length * 5) // 4
            assert len(encoded) == expected_encoded_len

    def test_bytearray_input(self):
        """Test that bytearray inputs work correctly."""
        original = bytearray(b"test with bytearray")
        encoded = z85encode(original)
        decoded = z85decode(encoded)
        assert decoded == bytes(original)
