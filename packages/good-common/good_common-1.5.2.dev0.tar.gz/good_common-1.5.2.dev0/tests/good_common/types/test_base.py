"""Tests for good_common.types._base module."""

import pytest
from pydantic import BaseModel

from good_common.types._base import (
    StringDict,
    Identifier,
    PythonImportableObjectType,
)


class TestStringDict:
    """Test StringDict type alias."""

    def test_string_dict_type(self):
        """Test StringDict is a dict with string keys and values."""
        test_dict: StringDict = {"key1": "value1", "key2": "value2"}
        
        assert isinstance(test_dict, dict)
        assert all(isinstance(k, str) for k in test_dict.keys())
        assert all(isinstance(v, str) for v in test_dict.values())


class TestIdentifier:
    """Test Identifier class."""

    def test_identifier_from_url_string(self):
        """Test creating Identifier from URL string."""
        url_str = "https://example.com/path?param=value"
        identifier = Identifier(url_str)
        
        assert identifier.scheme == "id"
        assert identifier.host == "example.com"
        assert identifier.path == "/path"
        assert "param" in identifier.query_params()

    def test_identifier_preserves_path(self):
        """Test that Identifier preserves the path."""
        identifier = Identifier("https://example.com/api/v1/resource")
        
        assert identifier.path == "/api/v1/resource"

    def test_identifier_normalizes_host(self):
        """Test that Identifier normalizes the host to lowercase."""
        identifier = Identifier("https://EXAMPLE.COM/path")
        
        # host_root should be lowercased
        assert "example" in str(identifier).lower()

    def test_identifier_strips_trailing_slash(self):
        """Test that Identifier strips trailing slashes from path."""
        identifier = Identifier("https://example.com/path/")
        
        assert identifier.path == "/path"

    def test_identifier_with_query_params(self):
        """Test Identifier with query parameters."""
        identifier = Identifier("https://example.com/path?foo=bar&baz=qux")
        
        query_params = identifier.query_params()
        assert "foo" in query_params
        assert "baz" in query_params

    def test_identifier_from_existing_url_object(self):
        """Test creating Identifier from existing URL object."""
        from good_common.types.web import URL
        
        url = URL("https://example.com/path")
        identifier = Identifier(url)
        
        assert identifier.scheme == "id"
        assert identifier.host == "example.com"
        assert identifier.path == "/path"

    def test_identifier_root_property(self):
        """Test Identifier root property."""
        identifier = Identifier("https://example.com/path?param1=value1&param2=value2")
        root = identifier.root
        
        # Root should have the same base but might filter query params
        assert root.scheme == "id"
        assert root.host == identifier.host


class TestPythonImportableObjectType:
    """Test PythonImportableObjectType class."""

    def test_create_from_function(self):
        """Test creating PythonImportableObjectType from a function."""
        def test_func():
            return "test"
        
        obj = PythonImportableObjectType(test_func)
        
        assert obj.func == test_func
        assert callable(obj.func)

    def test_create_from_class(self):
        """Test creating PythonImportableObjectType from a class."""
        class TestClass:
            pass
        
        obj = PythonImportableObjectType(TestClass)
        
        assert obj.func == TestClass
        assert callable(obj.func)

    def test_create_from_import_string(self):
        """Test creating PythonImportableObjectType from import string."""
        import_str = "json.dumps"
        obj = PythonImportableObjectType(import_str)
        
        import json
        assert obj.func == json.dumps
        assert callable(obj.func)

    def test_create_from_module_path(self):
        """Test creating from module:function format."""
        import_str = "json:loads"
        obj = PythonImportableObjectType(import_str)
        
        import json
        assert obj.func == json.loads

    def test_invalid_import_string(self):
        """Test handling invalid import string."""
        with pytest.raises((ImportError, AttributeError, ValueError)):
            obj = PythonImportableObjectType("nonexistent.module.function")
            obj.func  # This should trigger the import and raise an exception

    def test_call_imported_function(self):
        """Test calling an imported function."""
        obj = PythonImportableObjectType("json.dumps")
        
        result = obj.func({"key": "value"})
        assert result == '{"key": "value"}'

    def test_equality(self):
        """Test equality comparison."""
        obj1 = PythonImportableObjectType("json.dumps")
        obj2 = PythonImportableObjectType("json.dumps")
        obj3 = PythonImportableObjectType("json.loads")
        
        assert obj1 == obj2
        assert obj1 != obj3

    def test_string_representation(self):
        """Test string representation."""
        import json
        obj = PythonImportableObjectType(json.dumps)
        
        str_repr = str(obj)
        assert "json" in str_repr or "dumps" in str_repr

    def test_pydantic_integration(self):
        """Test using PythonImportableObjectType in Pydantic models."""
        
        class MyModel(BaseModel):
            processor: PythonImportableObjectType
        
        # Create model with function
        model = MyModel(processor="json.dumps")
        
        # Should be able to use the function
        result = model.processor.func({"test": "data"})
        assert result == '{"test": "data"}'

    def test_pydantic_validation_from_string(self):
        """Test Pydantic validation from string."""
        
        class MyModel(BaseModel):
            func: PythonImportableObjectType
        
        model = MyModel(func="os.path.join")
        
        import os
        assert model.func.func == os.path.join

    def test_pydantic_serialization(self):
        """Test serialization in Pydantic models."""
        
        class MyModel(BaseModel):
            func: PythonImportableObjectType
        
        model = MyModel(func="json.dumps")
        
        # Should serialize to the import path
        data = model.model_dump()
        assert "func" in data