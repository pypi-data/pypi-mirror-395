"""Tests for good_common.types._uuid module."""

import json
from uuid import UUID as StandardUUID

import pytest
from pydantic import BaseModel, ValidationError

from good_common.types._uuid import UUID, uuid4, uuid7


class TestUUID:
    """Test UUID class."""

    def test_uuid_creation_from_string(self):
        """Test creating UUID from string."""
        uuid_str = "550e8400-e29b-41d4-a716-446655440000"
        uuid_obj = UUID(uuid_str)
        
        assert str(uuid_obj) == uuid_str
        assert isinstance(uuid_obj, UUID)

    def test_uuid_creation_with_uuid4(self):
        """Test creating UUID with uuid4."""
        uuid_obj = uuid4()
        
        assert isinstance(uuid_obj, UUID)
        assert len(str(uuid_obj)) == 36
        assert uuid_obj.version == 4

    def test_uuid_creation_with_uuid7(self):
        """Test creating UUID with uuid7."""
        uuid_obj = uuid7()
        
        assert isinstance(uuid_obj, UUID)
        assert len(str(uuid_obj)) == 36
        assert uuid_obj.version == 7

    def test_uuid_encode(self):
        """Test UUID encode method."""
        uuid_str = "550e8400-e29b-41d4-a716-446655440000"
        uuid_obj = UUID(uuid_str)
        
        assert uuid_obj.encode() == uuid_str

    def test_uuid_equality(self):
        """Test UUID equality comparison."""
        uuid_str = "550e8400-e29b-41d4-a716-446655440000"
        uuid1 = UUID(uuid_str)
        uuid2 = UUID(uuid_str)
        uuid3 = uuid4()
        
        assert uuid1 == uuid2
        assert uuid1 != uuid3

    def test_uuid_standard_uuid_compatibility(self):
        """Test compatibility with standard library UUID."""
        uuid_str = "550e8400-e29b-41d4-a716-446655440000"
        custom_uuid = UUID(uuid_str)
        standard_uuid = StandardUUID(uuid_str)
        
        assert str(custom_uuid) == str(standard_uuid)
        assert custom_uuid.bytes == standard_uuid.bytes
        assert custom_uuid.hex == standard_uuid.hex
        assert custom_uuid.int == standard_uuid.int


class TestUUIDPydanticIntegration:
    """Test UUID Pydantic integration."""

    def test_uuid_in_pydantic_model(self):
        """Test using UUID in a Pydantic model."""
        
        class MyModel(BaseModel):
            id: UUID
            name: str
        
        uuid_obj = uuid4()
        model = MyModel(id=uuid_obj, name="test")
        
        assert model.id == uuid_obj
        assert isinstance(model.id, UUID)

    def test_uuid_validation_from_string(self):
        """Test UUID validation from string in Pydantic."""
        
        class MyModel(BaseModel):
            id: UUID
        
        uuid_str = "550e8400-e29b-41d4-a716-446655440000"
        model = MyModel(id=uuid_str)
        
        assert isinstance(model.id, UUID)
        assert str(model.id) == uuid_str

    def test_uuid_validation_invalid(self):
        """Test UUID validation with invalid input."""
        
        class MyModel(BaseModel):
            id: UUID
        
        with pytest.raises(ValidationError) as exc_info:
            MyModel(id="not-a-uuid")
        
        assert "UUID" in str(exc_info.value)

    def test_uuid_json_serialization(self):
        """Test UUID JSON serialization."""
        
        class MyModel(BaseModel):
            id: UUID
            name: str
        
        uuid_obj = UUID("550e8400-e29b-41d4-a716-446655440000")
        model = MyModel(id=uuid_obj, name="test")
        
        json_data = model.model_dump_json()
        data = json.loads(json_data)
        
        assert data["id"] == str(uuid_obj)
        assert data["name"] == "test"

    def test_uuid_json_deserialization(self):
        """Test UUID JSON deserialization."""
        
        class MyModel(BaseModel):
            id: UUID
            name: str
        
        json_data = '{"id": "550e8400-e29b-41d4-a716-446655440000", "name": "test"}'
        model = MyModel.model_validate_json(json_data)
        
        assert isinstance(model.id, UUID)
        assert str(model.id) == "550e8400-e29b-41d4-a716-446655440000"
        assert model.name == "test"


class TestUUIDHelpers:
    """Test UUID helper functions."""

    def test_uuid4_generates_unique_uuids(self):
        """Test that uuid4 generates unique UUIDs."""
        uuids = [uuid4() for _ in range(100)]
        unique_uuids = set(str(u) for u in uuids)
        
        assert len(unique_uuids) == 100
        assert all(u.version == 4 for u in uuids)

    def test_uuid7_generates_unique_uuids(self):
        """Test that uuid7 generates unique UUIDs."""
        uuids = [uuid7() for _ in range(100)]
        unique_uuids = set(str(u) for u in uuids)
        
        assert len(unique_uuids) == 100
        assert all(u.version == 7 for u in uuids)

    def test_uuid7_ordering(self):
        """Test that uuid7 UUIDs are time-ordered."""
        import time
        
        uuid1 = uuid7()
        time.sleep(0.01)  # Small delay to ensure different timestamps
        uuid2 = uuid7()
        
        # UUID7 should be time-ordered
        assert str(uuid1) < str(uuid2)