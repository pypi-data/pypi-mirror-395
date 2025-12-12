"""Test suite for jsonpath utilities (find, find_non_empty, Finder).

Updated for jsonpath-rust-bindings 1.0.2 with migration helpers.
"""

import pytest
from good_common.utilities import find, find_non_empty, find_with_regex, find_or_empty, Finder


class TestJsonPathUtilities:
    """Test cases for jsonpath-rust-binding wrapper functions."""

    @pytest.fixture
    def sample_data(self):
        """Sample JSON data for testing."""
        return {
            "store": {
                "book": [
                    {
                        "category": "reference",
                        "author": "Nigel Rees",
                        "title": "Sayings of the Century",
                        "price": 8.95,
                    },
                    {
                        "category": "fiction",
                        "author": "Evelyn Waugh",
                        "title": "Sword of Honour",
                        "price": 12.99,
                    },
                    {
                        "category": "fiction",
                        "author": "Herman Melville",
                        "title": "Moby Dick",
                        "isbn": "0-553-21311-3",
                        "price": 8.99,
                    },
                    {
                        "category": "fiction",
                        "author": "J. R. R. Tolkien",
                        "title": "The Lord of the Rings",
                        "isbn": "0-395-19395-8",
                        "price": 22.99,
                    },
                ],
                "bicycle": {"color": "red", "price": 19.95},
            },
            "expensive": 10,
        }

    @pytest.fixture
    def nested_data(self):
        """Nested data structure for testing."""
        return {
            "users": [
                {
                    "id": 1,
                    "name": "Alice",
                    "email": "alice@example.com",
                    "profile": {
                        "age": 30,
                        "city": "New York",
                        "hobbies": ["reading", "hiking"],
                    },
                },
                {
                    "id": 2,
                    "name": "Bob",
                    "email": "bob@example.com",
                    "profile": {
                        "age": 25,
                        "city": "San Francisco",
                        "hobbies": ["gaming", "cooking"],
                    },
                },
                {
                    "id": 3,
                    "name": "Charlie",
                    "email": None,  # Missing email
                    "profile": {
                        "age": 35,
                        "city": "",  # Empty city
                        "hobbies": [],  # Empty hobbies
                    },
                },
            ],
            "metadata": {
                "version": "1.0",
                "empty_field": None,
                "nested_empty": {"field": None, "another": ""},
            },
        }

    def test_find_basic_path(self, sample_data):
        """Test basic path queries."""
        # Direct path access
        result = find(sample_data, "$.expensive")
        assert len(result) == 1
        assert result[0].data == 10

        # Nested path access
        result = find(sample_data, "$.store.bicycle.color")
        assert len(result) == 1
        assert result[0].data == "red"

    def test_find_array_queries(self, sample_data):
        """Test array-based queries."""
        # All books
        result = find(sample_data, "$.store.book[*]")
        assert len(result) == 4

        # Specific book by index
        result = find(sample_data, "$.store.book[0]")
        assert len(result) == 1
        assert result[0].data["title"] == "Sayings of the Century"

        # Book range
        result = find(sample_data, "$.store.book[0:2]")
        assert len(result) == 2

        # Note: Negative indices are not supported in this version
        # Would need $.store.book[3] to get the last book instead

    def test_find_wildcard_queries(self, sample_data):
        """Test wildcard queries."""
        # All items in store
        result = find(sample_data, "$.store.*")
        assert len(result) == 2  # book array and bicycle object

        # All authors (recursive)
        result = find(sample_data, "$..author")
        assert len(result) == 4
        authors = [r.data for r in result]
        assert "Nigel Rees" in authors
        assert "J. R. R. Tolkien" in authors

    def test_find_filter_expressions(self, sample_data):
        """Test filter expressions."""
        # Books with ISBN
        result = find(sample_data, "$..book[?(@.isbn)]")
        assert len(result) == 2

        # Books cheaper than 10
        result = find(sample_data, "$.store.book[?(@.price < 10)]")
        assert len(result) == 2
        for r in result:
            assert r.data["price"] < 10

        # Books with specific author (regex match - using migration helper)
        # Old syntax no longer works: "$..book[?(@.author ~= '.*Melville')]"
        result = find_with_regex(sample_data, "$..book[*]", {"author": ".*Melville"})
        assert len(result) == 1
        assert result[0].data["author"] == "Herman Melville"
        
        # Test that the helper can also parse the old syntax
        result = find_with_regex(sample_data, "$..book[?(@.author ~= '.*Melville')]")
        assert len(result) == 1
        assert result[0].data["author"] == "Herman Melville"

    def test_find_recursive_descent(self, sample_data):
        """Test recursive descent queries."""
        # All prices
        result = find(sample_data, "$..price")
        assert len(result) == 5  # 4 books + 1 bicycle
        prices = [r.data for r in result]
        assert 19.95 in prices  # bicycle price
        assert 8.95 in prices  # first book price

    def test_find_non_empty_basic(self, nested_data):
        """Test find_non_empty with basic queries.
        
        Updated for 1.0.2: find_non_empty now properly filters out None values.
        """
        # find_non_empty should filter out None values
        result = find_non_empty(nested_data, "$.users[*].email")
        assert len(result) == 2  # Only returns non-None emails
        emails = [r.data for r in result]
        assert "alice@example.com" in emails
        assert "bob@example.com" in emails
        assert None not in emails  # Now filters None

    def test_find_non_empty_nested(self, nested_data):
        """Test find_non_empty with nested structures.
        
        Updated for 1.0.2: find_non_empty now filters empty strings and arrays.
        """
        # Cities (should exclude empty string)
        result = find_non_empty(nested_data, "$.users[*].profile.city")
        cities = [r.data for r in result]
        assert "New York" in cities
        assert "San Francisco" in cities
        assert "" not in cities  # Empty string is now filtered

        # Hobbies (should exclude empty array)
        result = find_non_empty(nested_data, "$.users[*].profile.hobbies")
        assert len(result) == 2  # Excludes empty array

    def test_find_non_empty_with_nulls(self, nested_data):
        """Test find_non_empty behavior with null values.
        
        Updated for 1.0.2: find_non_empty now filters null values.
        """
        # Metadata fields
        result = find(nested_data, "$.metadata.*")
        assert len(result) == 3  # All fields

        result = find_non_empty(nested_data, "$.metadata.*")
        assert len(result) == 2  # Excludes None value

    def test_finder_class_direct_usage(self, sample_data):
        """Test using Finder class directly."""
        finder = Finder(sample_data)

        # Test find method
        result = finder.find("$.store.book[*].author")
        assert len(result) == 4

        # Test that find_non_empty wrapper works correctly
        # (Finder.find_non_empty no longer exists in 1.0.2)
        data_with_nulls = {
            "items": [
                {"value": 1},
                {"value": None},
                {"value": 3},
                {"value": ""},
                {"value": 5},
            ]
        }
        # Use the wrapper function instead
        result = find_non_empty(data_with_nulls, "$.items[*].value")
        values = [r.data for r in result]
        assert len(values) == 3  # Filters out None and empty string
        assert 1 in values
        assert 3 in values
        assert 5 in values
        assert None not in values  # Excludes None
        assert "" not in values  # Excludes empty string

    def test_finder_reuse(self, sample_data):
        """Test that Finder instances can be reused efficiently."""
        finder = Finder(sample_data)

        # Multiple queries on same finder
        authors = finder.find("$..author")
        prices = finder.find("$..price")
        categories = finder.find("$..category")

        assert len(authors) == 4
        assert len(prices) == 5
        assert len(categories) == 4

    def test_complex_queries(self, sample_data):
        """Test complex JSONPath queries."""
        # Combination of filters and selections
        result = find(
            sample_data, "$.store.book[?(@.price < 10 && @.category == 'fiction')]"
        )
        assert len(result) == 1
        assert result[0].data["title"] == "Moby Dick"

        # Multiple array indices
        result = find(sample_data, "$.store.book[0,2]")
        assert len(result) == 2
        titles = [r.data["title"] for r in result]
        assert "Sayings of the Century" in titles
        assert "Moby Dick" in titles

    def test_empty_results(self, sample_data):
        """Test queries that return empty results.
        
        Updated for 1.0.2: Non-existent paths now return empty list.
        """
        # Non-existent path returns empty list
        result = find(sample_data, "$.nonexistent")
        assert len(result) == 0  # Now returns empty list

        # Filter with no matches
        result = find(sample_data, "$.store.book[?(@.price > 100)]")
        assert len(result) == 0  # Returns empty list for no matches

    def test_root_query(self, sample_data):
        """Test root element query."""
        result = find(sample_data, "$")
        assert len(result) == 1
        assert result[0].data == sample_data

    def test_path_attribute(self, sample_data):
        """Test that results include path information."""
        result = find(sample_data, "$.store.book[0].title")
        assert len(result) == 1
        assert hasattr(result[0], "path")
        # Path should indicate the location in the JSON structure

    def test_edge_cases(self):
        """Test edge cases and special scenarios."""
        # Empty object
        result = find({}, "$")
        assert len(result) == 1
        assert result[0].data == {}

        # Empty array query returns empty list
        data = {"items": []}
        result = find(data, "$.items[*]")
        assert len(result) == 0  # Returns empty list for empty array

        # Nested empty structures
        data = {"a": {"b": {"c": {}}}}
        result = find(data, "$.a.b.c")
        assert len(result) == 1
        assert result[0].data == {}

        # Special characters in keys
        data = {"key-with-dash": "value", "key.with.dots": "another"}
        result = find(data, "$['key-with-dash']")
        assert len(result) == 1
        assert result[0].data == "value"

    def test_array_slicing(self, sample_data):
        """Test various array slicing operations.
        
        Note: Negative indices are not supported in slices.
        """
        # From beginning
        result = find(sample_data, "$.store.book[:2]")
        assert len(result) == 2

        # From index to end
        result = find(sample_data, "$.store.book[2:]")
        assert len(result) == 2

    def test_performance_consideration(self, sample_data):
        """Test that demonstrates the performance consideration of reusing Finder."""
        # This is more of a documentation test
        # Creating multiple Finder instances (less efficient)
        for _ in range(3):
            result = find(sample_data, "$.store.book[*].author")
            assert len(result) == 4

        # Reusing a single Finder instance (more efficient)
        finder = Finder(sample_data)
        for _ in range(3):
            result = finder.find("$.store.book[*].author")
            assert len(result) == 4

    def test_data_immutability(self, sample_data):
        """Test that modifications to results don't affect original data."""
        original_price = sample_data["store"]["book"][0]["price"]

        # Find and modify result
        result = find(sample_data, "$.store.book[0]")
        result[0].data["price"] = 999.99

        # Original should be unchanged
        assert sample_data["store"]["book"][0]["price"] == original_price

    def test_unicode_and_special_chars(self):
        """Test handling of Unicode and special characters."""
        data = {
            "users": [
                {"name": "José", "city": "São Paulo"},
                {"name": "李明", "city": "北京"},
                {"name": "Müller", "city": "München"},
            ],
            "special!@#key": "value",
        }

        # Unicode in queries
        result = find(data, "$.users[*].name")
        assert len(result) == 3
        names = [r.data for r in result]
        assert "José" in names
        assert "李明" in names
        assert "Müller" in names

        # Special characters in keys
        result = find(data, "$['special!@#key']")
        assert len(result) == 1
        assert result[0].data == "value"
    
    def test_migration_helpers(self, sample_data):
        """Test migration helper functions for backward compatibility."""
        # Test find_with_regex helper
        result = find_with_regex(
            sample_data, 
            "$.store.book[*]", 
            {"author": ".*Tolkien"}
        )
        assert len(result) == 1
        assert result[0].data["title"] == "The Lord of the Rings"
        
        # Test parsing old regex syntax
        result = find_with_regex(
            sample_data,
            "$.store.book[?(@.author ~= '.*Rees')]"
        )
        assert len(result) == 1
        assert result[0].data["author"] == "Nigel Rees"
        
        # Test find_or_empty (though full compatibility isn't possible)
        result = find_or_empty(sample_data, "$.nonexistent.path")
        assert isinstance(result, list)
        
        # Test that find_non_empty filters properly
        data = {
            "values": [None, "", "test", 0, False, [], {}]
        }
        result = find_non_empty(data, "$.values[*]")
        values = [r.data for r in result]
        assert "test" in values
        assert 0 in values  # 0 is not empty
        assert False in values  # False is not empty
        assert None not in values
        assert "" not in values
        assert [] not in values
        assert {} not in values