"""Tests for utilities._regex module."""

import re


from good_common.utilities._regex import (
    REGEX_CAMEL_CASE,
    REGEX_NUMBERS_ONLY,
    REGEX_NUMERIC,
    RE_DOMAIN_NAMES,
    RE_EMAIL,
    RE_HTML,
    RE_JAVASCRIPT,
    RE_PHONE_NUMBER,
    RE_URL,
    RE_UUID,
    fullmatch_in,
    match_in,
    search_in,
)


class TestRegexPatterns:
    """Test predefined regex patterns."""

    def test_regex_numeric(self):
        """Test REGEX_NUMERIC pattern."""
        assert REGEX_NUMERIC.match("123")
        assert REGEX_NUMERIC.match("0")
        assert REGEX_NUMERIC.match("999999")
        assert not REGEX_NUMERIC.match("123.45")
        assert not REGEX_NUMERIC.match("12a3")
        assert not REGEX_NUMERIC.match("")

    def test_regex_numbers_only(self):
        """Test REGEX_NUMBERS_ONLY pattern."""
        assert REGEX_NUMBERS_ONLY.match("123")
        assert REGEX_NUMBERS_ONLY.match("123.45")
        assert REGEX_NUMBERS_ONLY.match("0.001")
        assert REGEX_NUMBERS_ONLY.match("...")
        assert not REGEX_NUMBERS_ONLY.match("12a3")
        assert not REGEX_NUMBERS_ONLY.match("12 34")

    def test_regex_camel_case(self):
        """Test REGEX_CAMEL_CASE pattern for splitting camel case."""
        # This pattern is used for splitting camel case strings
        text = "CamelCaseString"
        parts = REGEX_CAMEL_CASE.split(text)
        assert len(parts) > 1
        # Test various camel case patterns
        assert REGEX_CAMEL_CASE.search("camelCase")
        assert REGEX_CAMEL_CASE.search("HTTPResponse")
        assert REGEX_CAMEL_CASE.search("IOError")

    def test_re_domain_names(self):
        """Test RE_DOMAIN_NAMES pattern."""
        assert RE_DOMAIN_NAMES.match("example.com")
        assert RE_DOMAIN_NAMES.match("sub.example.com")
        assert RE_DOMAIN_NAMES.match("deep.sub.example.co.uk")
        assert RE_DOMAIN_NAMES.match("a-b.com")
        assert not RE_DOMAIN_NAMES.match("example")
        assert not RE_DOMAIN_NAMES.match("-example.com")
        assert not RE_DOMAIN_NAMES.match("example-.com")
        assert not RE_DOMAIN_NAMES.match("Example.COM")  # Case sensitive

    def test_re_uuid(self):
        """Test RE_UUID pattern."""
        assert RE_UUID.match("550e8400-e29b-41d4-a716-446655440000")
        assert RE_UUID.match("00000000-0000-0000-0000-000000000000")
        assert not RE_UUID.match("550e8400-e29b-41d4-a716-44665544000")  # Too short
        assert not RE_UUID.match("550e8400-e29b-41d4-a716-4466554400000")  # Too long
        assert not RE_UUID.match("550e8400e29b41d4a716446655440000")  # No dashes
        assert not RE_UUID.match("550E8400-E29B-41D4-A716-446655440000")  # Uppercase

    def test_re_email(self):
        """Test RE_EMAIL pattern."""
        assert RE_EMAIL.match("user@example.com")
        assert RE_EMAIL.match("test.user+tag@example.co.uk")
        assert RE_EMAIL.match("user_name@test-domain.com")
        assert RE_EMAIL.match("123@456.com")
        assert not RE_EMAIL.match("invalid.email")
        assert not RE_EMAIL.match("@example.com")
        assert not RE_EMAIL.match("user@")
        assert not RE_EMAIL.match("user @example.com")

    def test_re_html(self):
        """Test RE_HTML pattern."""
        assert RE_HTML.search("<div>")
        assert RE_HTML.search("<p class='test'>")
        assert RE_HTML.search("text <span>html</span> text")
        assert RE_HTML.search("</div>")
        assert not RE_HTML.search("no html here")
        assert not RE_HTML.search("< not a tag")

    def test_re_url(self):
        """Test RE_URL pattern."""
        assert RE_URL.match("http://example.com")
        assert RE_URL.match("https://example.com")
        assert RE_URL.match("http://www.example.com")
        assert RE_URL.match("https://example.com/path/to/page")
        assert RE_URL.match("https://example.com/path?query=value")
        assert RE_URL.match("http://sub.example.com/path")
        assert not RE_URL.match("ftp://example.com")
        assert not RE_URL.match("example.com")
        assert not RE_URL.match("http://")

    def test_re_phone_number(self):
        """Test RE_PHONE_NUMBER pattern."""
        assert RE_PHONE_NUMBER.match("123-456-7890")
        assert RE_PHONE_NUMBER.match("123.456.7890")
        assert RE_PHONE_NUMBER.match("123 456 7890")
        assert RE_PHONE_NUMBER.match("+1 123-456-7890")
        assert RE_PHONE_NUMBER.match("+44 123-456-7890")
        assert not RE_PHONE_NUMBER.match("123-456")
        assert not RE_PHONE_NUMBER.match("12-345-6789")

    def test_re_javascript(self):
        """Test RE_JAVASCRIPT pattern."""
        assert RE_JAVASCRIPT.match("function myFunc(")
        assert RE_JAVASCRIPT.match("  function test(")
        assert RE_JAVASCRIPT.match("function _private(")
        assert not RE_JAVASCRIPT.match("const func = ")
        assert not RE_JAVASCRIPT.match("myFunc(")


class TestRegExMatcher:
    """Test RegExMatcher class functionality."""

    def test_search_in_basic(self):
        """Test basic search_in functionality."""
        matcher = search_in("hello world")
        assert matcher == "world"
        assert matcher.match is not None
        assert matcher.match.group(0) == "world"

    def test_search_in_no_match(self):
        """Test search_in with no match."""
        matcher = search_in("hello world")
        assert not (matcher == "xyz")
        assert matcher.match is None

    def test_search_in_with_pattern_object(self):
        """Test search_in with compiled pattern."""
        matcher = search_in("hello world")
        pattern = re.compile(r"w\w+")
        assert matcher == pattern
        assert matcher.match is not None

    def test_search_in_with_tuple_pattern(self):
        """Test search_in with tuple pattern (pattern, flags)."""
        matcher = search_in("Hello World")
        assert matcher == (r"world", re.IGNORECASE)
        assert matcher.match is not None

    def test_match_in_basic(self):
        """Test basic match_in functionality."""
        matcher = match_in("hello world")
        assert matcher == "hello"
        assert matcher.match is not None

    def test_match_in_not_at_start(self):
        """Test match_in fails when pattern not at start."""
        matcher = match_in("hello world")
        assert not (matcher == "world")
        assert matcher.match is None

    def test_fullmatch_in_exact(self):
        """Test fullmatch_in with exact match."""
        matcher = fullmatch_in("hello")
        assert matcher == "hello"
        assert matcher.match is not None

    def test_fullmatch_in_partial_fails(self):
        """Test fullmatch_in fails on partial match."""
        matcher = fullmatch_in("hello world")
        assert not (matcher == "hello")
        assert matcher.match is None

    def test_matcher_getitem_single_group(self):
        """Test getting single group from match."""
        matcher = search_in("test123")
        matcher == r"([a-z]+)(\d+)"
        assert matcher[0] == "test123"
        assert matcher[1] == "test"
        assert matcher[2] == "123"

    def test_matcher_getitem_named_group(self):
        """Test getting named group from match."""
        matcher = search_in("test123")
        matcher == r"(?P<word>[a-z]+)(?P<num>\d+)"
        assert matcher["word"] == "test"
        assert matcher["num"] == "123"

    def test_matcher_getitem_tuple_groups(self):
        """Test getting multiple groups as tuple."""
        matcher = search_in("test123")
        matcher == r"([a-z]+)(\d+)"
        result = matcher[(1, 2)]
        assert result == ("test", "123")

    def test_matcher_getitem_no_match_returns_none(self):
        """Test getting group when no match returns None."""
        matcher = search_in("test")
        matcher == r"\d+"
        assert matcher[0] is None
        assert matcher[1] is None

    def test_matcher_eq_with_invalid_type(self):
        """Test equality with invalid type returns NotImplemented."""
        matcher = search_in("test")
        result = matcher.__eq__(123)
        assert result is NotImplemented
        result = matcher.__eq__([])
        assert result is NotImplemented
        result = matcher.__eq__({})
        assert result is NotImplemented

    def test_matcher_multiple_comparisons(self):
        """Test multiple comparisons with same matcher."""
        matcher = search_in("hello world test")
        assert matcher == "hello"
        assert matcher == "world"
        assert matcher == "test"
        assert not (matcher == "missing")

    def test_matcher_caching_behavior(self):
        """Test that match result is cached in matcher."""
        matcher = search_in("test123")
        matcher == r"(\d+)"
        first_match = matcher.match
        assert first_match is not None
        # Same match should be cached
        assert matcher.match is first_match
        # New comparison updates the cache
        matcher == r"(\w+)"
        assert matcher.match is not first_match

    def test_search_in_with_groups(self):
        """Test search_in with capture groups."""
        matcher = search_in("Price: $19.99")
        matcher == r"\$(\d+\.\d+)"
        assert matcher[1] == "19.99"

    def test_match_in_anchored_pattern(self):
        """Test match_in with anchored pattern."""
        matcher = match_in("start middle end")
        assert matcher == r"^start"
        assert matcher[0] == "start"

    def test_fullmatch_in_complete_string(self):
        """Test fullmatch_in requires complete string match."""
        matcher = fullmatch_in("abc123")
        assert matcher == r"[a-z]+\d+"
        assert not (matcher == r"[a-z]+")
        assert not (matcher == r"\d+")


class TestRegExMatcherEdgeCases:
    """Test edge cases for RegExMatcher."""

    def test_empty_string_search(self):
        """Test searching in empty string."""
        matcher = search_in("")
        assert not (matcher == "test")

    def test_empty_pattern(self):
        """Test empty pattern matches empty string."""
        matcher = search_in("test")
        assert matcher == ""  # Empty pattern matches

    def test_complex_regex_pattern(self):
        """Test complex regex pattern."""
        matcher = search_in("email: user@example.com")
        assert matcher == r"\b[\w.%+-]+@[\w.-]+\.[A-Za-z]{2,}\b"
        assert matcher.match is not None

    def test_multiple_named_groups(self):
        """Test multiple named groups extraction."""
        matcher = search_in("2024-01-15")
        matcher == r"(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})"
        assert matcher["year"] == "2024"
        assert matcher["month"] == "01"
        assert matcher["day"] == "15"

    def test_getitem_with_tuple_of_strings(self):
        """Test getting multiple named groups as tuple."""
        matcher = search_in("John Doe")
        matcher == r"(?P<first>\w+)\s+(?P<last>\w+)"
        result = matcher[("first", "last")]
        assert result == ("John", "Doe")
