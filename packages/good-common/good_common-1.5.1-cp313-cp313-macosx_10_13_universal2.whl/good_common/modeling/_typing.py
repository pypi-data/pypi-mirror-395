from pydantic import BaseModel
from typing import (
    Any,
    Dict,
    List,
    Set,
    Tuple,
    Union,
    get_args,
    get_origin,
)
import types
import decimal
from enum import Enum


class TypeInfo:
    @classmethod
    def annotation_extract_primary_type(
        cls, annotation: Any, metadata: list[Any] | None = None
    ) -> "TypeInfo":
        """Extract the primary type from a type annotation, handling Optional types."""
        metadata = metadata or []
        origin = get_origin(annotation)

        # Handle Union/Optional types
        if origin is Union:
            args = get_args(annotation)
            # Check if it's Optional[T] (Union[T, None])
            if type(None) in args:
                non_none_args = [arg for arg in args if arg is not type(None)]
                if len(non_none_args) == 1:
                    return TypeInfo(non_none_args[0], is_optional=True)
            return TypeInfo(annotation, is_optional=False, metadata=metadata)
        else:
            return TypeInfo(annotation, is_optional=False, metadata=metadata)

    def __init__(self, annotation: Any, is_optional: bool, metadata: list[Any] = []):
        self.type = annotation
        self.is_optional = is_optional
        self.is_pydantic_model = False
        self.item_type = None
        self.db_type = None
        self.metadata = metadata

        # Store the original type before potential unwrapping
        original_type = self.type

        # Check if we're dealing with Optional/Union that wasn't processed by annotation_extract_primary_type
        origin = get_origin(self.type)
        if (
            origin is Union or origin == types.UnionType
        ):  # Handle both Union representations
            args = get_args(self.type)
            if type(None) in args:
                non_none_args = [arg for arg in args if arg is not type(None)]
                if len(non_none_args) == 1:
                    self.type = non_none_args[0]
                    self.is_optional = True
                    # Update origin after modifying self.type
                    origin = get_origin(self.type)

        # Check if type has a custom ClickHouse type
        if hasattr(self.type, "__clickhouse_type__"):
            self.db_type = getattr(self.type, "__clickhouse_type__")

        if hasattr(self.type, "__is_mapping__") and self.type.__is_mapping__:
            self.is_mapping = True

        # Check if type is a Pydantic model - check both unwrapped type and original type
        if isinstance(self.type, type) and issubclass(self.type, BaseModel):
            self.is_pydantic_model = True
        # In case the unwrapped type doesn't properly detect the Pydantic model
        elif (
            self.is_optional
            and isinstance(original_type, type)
            and hasattr(original_type, "__args__")
        ):
            for arg in get_args(original_type):
                if (
                    arg is not type(None)
                    and isinstance(arg, type)
                    and issubclass(arg, BaseModel)
                ):
                    self.is_pydantic_model = True
                    break

        # Handle collection types
        if origin is not None:
            self.origin_type = origin
            type_args = get_args(self.type)

            # Process container types (List, Set, Tuple, Dict, etc.)
            if origin in (list, set, frozenset, List, Set) and type_args:
                self.is_sequence = True
                self.item_type = self.annotation_extract_primary_type(type_args[0])

            elif origin in (tuple, Tuple) and type_args:
                self.is_tuple = True
                self.item_types = [
                    self.annotation_extract_primary_type(arg) for arg in type_args
                ]
                # Handle Tuple[T, ...] syntax
                if len(type_args) == 2 and type_args[1] is Ellipsis:
                    self.is_sequence = True
                    self.item_type = self.annotation_extract_primary_type(type_args[0])

            elif origin in (dict, Dict) and len(type_args) == 2:
                self.is_mapping = True
                self.key_type = self.annotation_extract_primary_type(type_args[0])
                self.value_type = self.annotation_extract_primary_type(type_args[1])

    type: Any
    is_optional: bool
    origin_type: Any = None
    item_type: "TypeInfo | None" = None
    item_types: list["TypeInfo"] | None = None
    key_type: "TypeInfo | None" = None
    value_type: "TypeInfo | None" = None
    is_pydantic_model: bool = False
    is_sequence: bool = False
    is_tuple: bool = False
    is_mapping: bool = False
    db_type: str | None = None
    metadata: list[Any] = []

    @property
    def json_serialize(self) -> bool:
        """Check if the type can be serialized to JSON."""
        if self.is_pydantic_model:
            return False
        if self.is_mapping:
            return False
        if self.is_sequence:
            return self.item_type.json_serialize if self.item_type else False
        if self.is_tuple:
            return (
                all(item.json_serialize for item in self.item_types)
                if self.item_types
                else False
            )
        return self.type in (
            # str,
            # int,
            # float,
            # bool,
            # type(None),
            # uuid.UUID,
            # ULID,
            decimal.Decimal,
            # datetime.datetime,
            # datetime.date,
            Enum,
            # dict,
        )

    def __repr__(self):
        return (
            f"TypeInfo({self.type}, is_optional={self.is_optional}, "
            f"is_pydantic_model={self.is_pydantic_model}, "
            f"is_sequence={self.is_sequence}, is_mapping={self.is_mapping})"
        )
