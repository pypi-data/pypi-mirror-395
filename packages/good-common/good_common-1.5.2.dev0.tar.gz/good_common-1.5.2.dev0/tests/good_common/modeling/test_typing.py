"""Tests for modeling._typing module."""

import datetime
import decimal
import uuid
from enum import Enum
from typing import Annotated, Dict, List, Optional, Set, Tuple, Union

from pydantic import BaseModel
from ulid import ULID

from good_common.modeling._typing import TypeInfo


# Test models and types
class SimpleModel(BaseModel):
    """Simple Pydantic model for testing."""

    name: str
    age: int


class NestedModel(BaseModel):
    """Nested Pydantic model for testing."""

    user: SimpleModel
    tags: List[str]


class CustomEnum(Enum):
    """Test enum."""

    OPTION_A = "a"
    OPTION_B = "b"


class CustomTypeWithClickhouse:
    """Custom type with ClickHouse type annotation."""

    __clickhouse_type__ = "String"


class CustomMappingType:
    """Custom type marked as mapping."""

    __is_mapping__ = True


class TestTypeInfoBasicTypes:
    """Test TypeInfo with basic Python types."""

    def test_simple_string_type(self):
        """Test TypeInfo with str type."""
        type_info = TypeInfo(str, is_optional=False)
        assert type_info.type is str
        assert type_info.is_optional is False
        assert type_info.is_pydantic_model is False
        assert type_info.origin_type is None

    def test_simple_int_type(self):
        """Test TypeInfo with int type."""
        type_info = TypeInfo(int, is_optional=False)
        assert type_info.type is int
        assert type_info.is_optional is False

    def test_simple_float_type(self):
        """Test TypeInfo with float type."""
        type_info = TypeInfo(float, is_optional=False)
        assert type_info.type is float
        assert type_info.is_optional is False

    def test_simple_bool_type(self):
        """Test TypeInfo with bool type."""
        type_info = TypeInfo(bool, is_optional=False)
        assert type_info.type is bool
        assert type_info.is_optional is False

    def test_uuid_type(self):
        """Test TypeInfo with UUID type."""
        type_info = TypeInfo(uuid.UUID, is_optional=False)
        assert type_info.type is uuid.UUID
        assert type_info.is_optional is False

    def test_ulid_type(self):
        """Test TypeInfo with ULID type."""
        type_info = TypeInfo(ULID, is_optional=False)
        assert type_info.type is ULID
        assert type_info.is_optional is False

    def test_decimal_type(self):
        """Test TypeInfo with Decimal type."""
        type_info = TypeInfo(decimal.Decimal, is_optional=False)
        assert type_info.type is decimal.Decimal
        assert type_info.is_optional is False

    def test_datetime_type(self):
        """Test TypeInfo with datetime type."""
        type_info = TypeInfo(datetime.datetime, is_optional=False)
        assert type_info.type is datetime.datetime
        assert type_info.is_optional is False

    def test_date_type(self):
        """Test TypeInfo with date type."""
        type_info = TypeInfo(datetime.date, is_optional=False)
        assert type_info.type is datetime.date
        assert type_info.is_optional is False


class TestTypeInfoOptionalTypes:
    """Test TypeInfo with Optional types."""

    def test_optional_string_with_union(self):
        """Test Optional[str] using Union syntax."""
        type_info = TypeInfo(Optional[str], is_optional=False)
        # TypeInfo should unwrap Optional[str] to str
        assert type_info.type is str
        assert type_info.is_optional is True

    def test_optional_int(self):
        """Test Optional[int]."""
        type_info = TypeInfo(Optional[int], is_optional=False)
        assert type_info.type is int
        assert type_info.is_optional is True

    def test_union_with_none(self):
        """Test Union[str, None] (equivalent to Optional[str])."""
        type_info = TypeInfo(Union[str, None], is_optional=False)
        assert type_info.type is str
        assert type_info.is_optional is True

    def test_explicit_optional_flag(self):
        """Test TypeInfo with explicit is_optional flag."""
        type_info = TypeInfo(str, is_optional=True)
        assert type_info.type is str
        assert type_info.is_optional is True

    def test_union_multiple_types_no_none(self):
        """Test Union with multiple types but no None."""
        type_info = TypeInfo(Union[str, int], is_optional=False)
        # Should keep as Union since it's not Optional
        assert type_info.type == Union[str, int]
        assert type_info.is_optional is False


class TestTypeInfoPydanticModels:
    """Test TypeInfo with Pydantic models."""

    def test_simple_pydantic_model(self):
        """Test TypeInfo with Pydantic model."""
        type_info = TypeInfo(SimpleModel, is_optional=False)
        assert type_info.type == SimpleModel
        assert type_info.is_pydantic_model is True
        assert type_info.is_optional is False

    def test_optional_pydantic_model(self):
        """Test Optional Pydantic model."""
        type_info = TypeInfo(Optional[SimpleModel], is_optional=False)
        assert type_info.type == SimpleModel
        assert type_info.is_pydantic_model is True
        assert type_info.is_optional is True

    def test_nested_pydantic_model(self):
        """Test nested Pydantic model."""
        type_info = TypeInfo(NestedModel, is_optional=False)
        assert type_info.type == NestedModel
        assert type_info.is_pydantic_model is True


class TestTypeInfoListTypes:
    """Test TypeInfo with List/sequence types."""

    def test_list_of_strings(self):
        """Test List[str]."""
        type_info = TypeInfo(List[str], is_optional=False)
        assert type_info.origin_type is list
        assert type_info.is_sequence is True
        assert type_info.item_type is not None
        assert type_info.item_type.type is str

    def test_list_of_ints(self):
        """Test List[int]."""
        type_info = TypeInfo(List[int], is_optional=False)
        assert type_info.is_sequence is True
        assert type_info.item_type.type is int

    def test_list_of_pydantic_models(self):
        """Test List[Model]."""
        type_info = TypeInfo(List[SimpleModel], is_optional=False)
        assert type_info.is_sequence is True
        assert type_info.item_type.is_pydantic_model is True
        assert type_info.item_type.type == SimpleModel

    def test_set_of_strings(self):
        """Test Set[str]."""
        type_info = TypeInfo(Set[str], is_optional=False)
        assert type_info.origin_type is set
        assert type_info.is_sequence is True
        assert type_info.item_type.type is str

    def test_optional_list(self):
        """Test Optional[List[str]]."""
        type_info = TypeInfo(Optional[List[str]], is_optional=False)
        assert type_info.is_optional is True
        assert type_info.is_sequence is True
        assert type_info.item_type.type is str

    def test_list_of_optional_items(self):
        """Test List[Optional[str]]."""
        type_info = TypeInfo(List[Optional[str]], is_optional=False)
        assert type_info.is_sequence is True
        assert type_info.item_type.is_optional is True
        assert type_info.item_type.type is str


class TestTypeInfoTupleTypes:
    """Test TypeInfo with Tuple types."""

    def test_tuple_fixed_size(self):
        """Test Tuple[str, int] with fixed size."""
        type_info = TypeInfo(Tuple[str, int], is_optional=False)
        assert type_info.origin_type is tuple
        assert type_info.is_tuple is True
        assert type_info.item_types is not None
        assert len(type_info.item_types) == 2
        assert type_info.item_types[0].type is str
        assert type_info.item_types[1].type is int

    def test_tuple_variable_length(self):
        """Test Tuple[str, ...] variable length."""
        type_info = TypeInfo(Tuple[str, ...], is_optional=False)
        assert type_info.is_tuple is True
        assert type_info.is_sequence is True  # Variable length tuples are sequences
        assert type_info.item_type.type is str

    def test_tuple_mixed_types(self):
        """Test Tuple with mixed types."""
        type_info = TypeInfo(Tuple[str, int, float, bool], is_optional=False)
        assert type_info.is_tuple is True
        assert len(type_info.item_types) == 4
        assert type_info.item_types[2].type is float
        assert type_info.item_types[3].type is bool


class TestTypeInfoDictTypes:
    """Test TypeInfo with Dict/mapping types."""

    def test_dict_string_to_int(self):
        """Test Dict[str, int]."""
        type_info = TypeInfo(Dict[str, int], is_optional=False)
        assert type_info.origin_type is dict
        assert type_info.is_mapping is True
        assert type_info.key_type.type is str
        assert type_info.value_type.type is int

    def test_dict_string_to_model(self):
        """Test Dict[str, Model]."""
        type_info = TypeInfo(Dict[str, SimpleModel], is_optional=False)
        assert type_info.is_mapping is True
        assert type_info.key_type.type is str
        assert type_info.value_type.is_pydantic_model is True
        assert type_info.value_type.type == SimpleModel

    def test_dict_with_optional_values(self):
        """Test Dict[str, Optional[int]]."""
        type_info = TypeInfo(Dict[str, Optional[int]], is_optional=False)
        assert type_info.is_mapping is True
        assert type_info.value_type.is_optional is True
        assert type_info.value_type.type is int

    def test_optional_dict(self):
        """Test Optional[Dict[str, int]]."""
        type_info = TypeInfo(Optional[Dict[str, int]], is_optional=False)
        assert type_info.is_optional is True
        assert type_info.is_mapping is True
        assert type_info.key_type.type is str
        assert type_info.value_type.type is int


class TestTypeInfoAnnotationExtract:
    """Test annotation_extract_primary_type classmethod."""

    def test_extract_simple_type(self):
        """Test extracting simple type."""
        type_info = TypeInfo.annotation_extract_primary_type(str)
        assert type_info.type is str
        assert type_info.is_optional is False

    def test_extract_optional_type(self):
        """Test extracting Optional type."""
        type_info = TypeInfo.annotation_extract_primary_type(Optional[str])
        assert type_info.type is str
        assert type_info.is_optional is True

    def test_extract_union_with_none(self):
        """Test extracting Union[T, None]."""
        type_info = TypeInfo.annotation_extract_primary_type(Union[int, None])
        assert type_info.type is int
        assert type_info.is_optional is True

    def test_extract_union_without_none(self):
        """Test extracting Union without None."""
        type_info = TypeInfo.annotation_extract_primary_type(Union[str, int])
        assert type_info.type == Union[str, int]
        assert type_info.is_optional is False

    def test_extract_with_metadata(self):
        """Test extracting type with metadata."""
        metadata = ["test_metadata"]
        type_info = TypeInfo.annotation_extract_primary_type(str, metadata=metadata)
        assert type_info.metadata == metadata

    def test_extract_annotated_type(self):
        """Test extracting Annotated type."""
        annotated_type = Annotated[str, "description"]
        type_info = TypeInfo.annotation_extract_primary_type(annotated_type)
        # Annotated should be unwrapped to the base type
        assert type_info.type == annotated_type


class TestTypeInfoCustomTypes:
    """Test TypeInfo with custom types and special attributes."""

    def test_type_with_clickhouse_annotation(self):
        """Test type with __clickhouse_type__ attribute."""
        type_info = TypeInfo(CustomTypeWithClickhouse, is_optional=False)
        assert type_info.db_type == "String"

    def test_type_with_mapping_flag(self):
        """Test type with __is_mapping__ flag."""
        type_info = TypeInfo(CustomMappingType, is_optional=False)
        assert type_info.is_mapping is True

    def test_enum_type(self):
        """Test Enum type."""
        type_info = TypeInfo(CustomEnum, is_optional=False)
        assert type_info.type == CustomEnum
        assert type_info.is_optional is False


class TestTypeInfoJsonSerialize:
    """Test json_serialize property."""

    def test_decimal_json_serialize(self):
        """Test that Decimal is marked for JSON serialization."""
        type_info = TypeInfo(decimal.Decimal, is_optional=False)
        assert type_info.json_serialize is True

    def test_enum_json_serialize(self):
        """Test that Enum is marked for JSON serialization."""
        type_info = TypeInfo(Enum, is_optional=False)
        assert type_info.json_serialize is True

    def test_pydantic_model_not_json_serialize(self):
        """Test that Pydantic models are not marked for JSON serialization."""
        type_info = TypeInfo(SimpleModel, is_optional=False)
        assert type_info.json_serialize is False

    def test_mapping_not_json_serialize(self):
        """Test that mappings are not marked for JSON serialization."""
        type_info = TypeInfo(Dict[str, int], is_optional=False)
        assert type_info.json_serialize is False

    def test_sequence_json_serialize_depends_on_item(self):
        """Test that sequence JSON serialization depends on item type."""
        # List of Decimals should serialize
        type_info = TypeInfo(List[decimal.Decimal], is_optional=False)
        assert type_info.json_serialize is True

        # List of Pydantic models should not serialize
        type_info = TypeInfo(List[SimpleModel], is_optional=False)
        assert type_info.json_serialize is False

    def test_tuple_json_serialize_depends_on_items(self):
        """Test that tuple JSON serialization depends on all item types."""
        # Tuple of Decimals should serialize
        type_info = TypeInfo(Tuple[decimal.Decimal, decimal.Decimal], is_optional=False)
        assert type_info.json_serialize is True


class TestTypeInfoRepr:
    """Test TypeInfo __repr__ method."""

    def test_repr_simple_type(self):
        """Test __repr__ for simple type."""
        type_info = TypeInfo(str, is_optional=False)
        repr_str = repr(type_info)
        assert "TypeInfo" in repr_str
        assert "str" in repr_str
        assert "is_optional=False" in repr_str

    def test_repr_optional_type(self):
        """Test __repr__ for optional type."""
        type_info = TypeInfo(Optional[int], is_optional=False)
        repr_str = repr(type_info)
        assert "is_optional=True" in repr_str

    def test_repr_pydantic_model(self):
        """Test __repr__ for Pydantic model."""
        type_info = TypeInfo(SimpleModel, is_optional=False)
        repr_str = repr(type_info)
        assert "is_pydantic_model=True" in repr_str

    def test_repr_sequence(self):
        """Test __repr__ for sequence type."""
        type_info = TypeInfo(List[str], is_optional=False)
        repr_str = repr(type_info)
        assert "is_sequence=True" in repr_str

    def test_repr_mapping(self):
        """Test __repr__ for mapping type."""
        type_info = TypeInfo(Dict[str, int], is_optional=False)
        repr_str = repr(type_info)
        assert "is_mapping=True" in repr_str


class TestTypeInfoEdgeCases:
    """Test edge cases and complex scenarios."""

    def test_nested_optional_lists(self):
        """Test Optional[List[Optional[str]]]."""
        type_info = TypeInfo(Optional[List[Optional[str]]], is_optional=False)
        assert type_info.is_optional is True
        assert type_info.is_sequence is True
        assert type_info.item_type.is_optional is True
        assert type_info.item_type.type is str

    def test_list_of_tuples(self):
        """Test List[Tuple[str, int]]."""
        type_info = TypeInfo(List[Tuple[str, int]], is_optional=False)
        assert type_info.is_sequence is True
        assert type_info.item_type.is_tuple is True
        assert len(type_info.item_type.item_types) == 2

    def test_dict_with_list_values(self):
        """Test Dict[str, List[int]]."""
        type_info = TypeInfo(Dict[str, List[int]], is_optional=False)
        assert type_info.is_mapping is True
        assert type_info.value_type.is_sequence is True
        assert type_info.value_type.item_type.type is int

    def test_metadata_preservation(self):
        """Test that metadata is preserved."""
        metadata = ["annotation1", "annotation2"]
        type_info = TypeInfo(str, is_optional=False, metadata=metadata)
        assert type_info.metadata == metadata

    def test_none_type(self):
        """Test handling of NoneType."""
        type_info = TypeInfo(type(None), is_optional=False)
        assert type_info.type is type(None)
        assert type_info.is_optional is False

    def test_complex_nested_structure(self):
        """Test complex nested type structure."""
        complex_type = Dict[str, List[Optional[SimpleModel]]]
        type_info = TypeInfo(complex_type, is_optional=False)
        assert type_info.is_mapping is True
        assert type_info.value_type.is_sequence is True
        assert type_info.value_type.item_type.is_optional is True
        assert type_info.value_type.item_type.is_pydantic_model is True
