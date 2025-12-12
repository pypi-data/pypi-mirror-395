from typing import Any, Self, Required, TypedDict, Literal, Dict
from uuid import UUID as _DEFAULT_UUID

try:
    from uuid_utils import UUID as _UUID
    from uuid_utils import uuid7 as _uuid7, uuid4 as _uuid4
except ModuleNotFoundError as e:  # pragma: no cover
    raise RuntimeError(
        'The `ulid` module requires "uuid_utils" to be installed. '
        'You can install it with "pip install python-ulid".'
    ) from e
from pydantic import GetCoreSchemaHandler
from pydantic_core import PydanticCustomError, SchemaSerializer, core_schema

# from pydantic import UUID1


class UuidSchema(TypedDict, total=False):
    type: Required[Literal["uuid"]]
    version: Literal[1, 3, 4, 5, 6, 7]
    strict: bool
    ref: str
    metadata: Dict[str, Any]
    serialization: core_schema.SerSchema


class UUID(_UUID):
    def encode(self) -> str:
        return str(self)

    # def __get_pydantic_json_schema__(
    #     self,
    #     core_schema: core_schema.CoreSchema,
    #     handler: GetJsonSchemaHandler | None = None,
    # ) -> JsonSchemaValue:

    #     field_schema = handler(core_schema)
    #     field_schema.pop("anyOf", None)  # remove the bytes/str union
    #     field_schema.update(type="string", format=f"uuid{self.uuid_version}")
    #     return field_schema

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        source: type[Any],
        handler: GetCoreSchemaHandler,
    ) -> core_schema.CoreSchema:
        from_str_schema = core_schema.chain_schema(
            [
                core_schema.str_schema(),
                core_schema.no_info_plain_validator_function(cls._validate_from_str),
            ]
        )

        schema = core_schema.union_schema(
            [
                core_schema.is_instance_schema(cls),
                core_schema.is_instance_schema(_DEFAULT_UUID),
                core_schema.is_instance_schema(_UUID),
                from_str_schema,
                core_schema.chain_schema(
                    [
                        core_schema.int_schema(),
                        core_schema.no_info_plain_validator_function(
                            cls._validate_from_int
                        ),
                    ]
                ),
                core_schema.chain_schema(
                    [
                        core_schema.bytes_schema(),
                        core_schema.no_info_plain_validator_function(
                            cls._validate_from_bytes
                        ),
                    ]
                ),
            ],
            serialization=core_schema.plain_serializer_function_ser_schema(
                str,
                info_arg=False,
                return_schema=core_schema.str_schema(),
                when_used="json",
            ),
        )
        cls.__pydantic_serializer__ = SchemaSerializer(  # type: ignore[attr-defined]
            schema
        )  # <-- this is necessary for pydantic-core to serialize

        return schema

    @classmethod
    def _validate_from_str(cls, value: str) -> "UUID":
        """Validate UUID from string."""
        try:
            return cls(value)
        except ValueError as e:
            raise PydanticCustomError(
                "uuid_format",
                "Unrecognized format",
            ) from e

    @classmethod
    def _validate_from_int(cls, value: int) -> "UUID":
        """Validate UUID from integer."""
        try:
            return cls(int=value)
        except ValueError as e:
            raise PydanticCustomError(
                "uuid_format",
                "Unrecognized format",
            ) from e

    @classmethod
    def _validate_from_bytes(cls, value: bytes) -> "UUID":
        """Validate UUID from bytes."""
        try:
            return cls(bytes=value)
        except ValueError as e:
            raise PydanticCustomError(
                "uuid_format",
                "Unrecognized format",
            ) from e

    @classmethod
    def create_v7(cls) -> Self:
        return cls(int=_uuid7().int)


def uuid4() -> UUID:
    """Generate a UUID version 4 (random UUID)."""
    return UUID(int=_uuid4().int)


def uuid7() -> UUID:
    """Generate a UUID version 7 (timestamp-based UUID)."""
    return UUID(int=_uuid7().int)
