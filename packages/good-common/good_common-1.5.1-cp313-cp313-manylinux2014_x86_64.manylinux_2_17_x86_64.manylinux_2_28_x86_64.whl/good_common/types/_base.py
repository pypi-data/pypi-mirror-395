from importlib import import_module
from typing import Any, Callable, Annotated, TYPE_CHECKING, Optional, cast

from pydantic import GetCoreSchemaHandler, BeforeValidator
from pydantic_core import CoreSchema, core_schema

type StringDict = dict[str, str]


# Lazy import to avoid circular dependency at module level
def _get_identifier_base():
    """Get the Identifier base class (URL) lazily."""
    from .web import URL

    return URL


if TYPE_CHECKING:
    from .web import URL

    class Identifier(URL):
        """Type checking version of Identifier."""

        pass
else:
    # Runtime version with lazy import
    class Identifier:
        """
        Identifier type that lazily inherits from URL.
        """

        _url_class = None

        def __new__(cls, url: Any, strict: bool = False):
            # Lazy import URL
            if cls._url_class is None:
                from .web import URL

                cls._url_class = URL

            URL = cls._url_class

            if isinstance(url, URL):
                _url = url
            else:
                _url = URL(url)

            # Create URL instance with id scheme
            instance = URL.build(
                scheme="id",
                username=_url.username,
                password=_url.password,
                host=_url.host_root.lower(),
                path=_url.path.rstrip("/"),
                query=_url.query_params("flat"),
            )

            # Override root property
            def get_root():
                return URL(instance).update(
                    query={
                        k: v
                        for k, v in instance.query_params("flat").items()
                        if not k.startswith("zz_")
                    }
                )

            # Create a new class that extends the URL class with custom root property
            class IdentifierWithRoot(instance.__class__):
                @property
                def root(self):
                    return get_root()

            instance.__class__ = IdentifierWithRoot
            instance.domain = instance.host

            return instance


class PythonImportableObjectType(str):
    """
    function or class
    """

    _path: str
    _func: str
    _original_obj: Optional[Callable]

    def __new__(cls, obj: Any):
        # Store the original object if it's not a string
        original_obj = None
        if not isinstance(obj, str):
            if hasattr(obj, "__module__") and hasattr(obj, "__name__"):
                original_obj = obj
                obj = f"{obj.__module__}:{obj.__name__}"
            else:
                raise ValueError(f"Cannot convert {obj} to PythonImportableObject")
        instance = super().__new__(cls, obj)
        if ":" in obj:
            instance._path, instance._func = obj.rsplit(":", 1)
        else:
            instance._path, instance._func = obj.rsplit(".", 1)
        instance._original_obj = original_obj
        return instance

    @property
    def func(self) -> Callable:
        """Get the resolved function/class object."""
        if self._original_obj is not None:
            return self._original_obj
        return self.resolve()

    def resolve(self) -> Callable:
        module = import_module(self._path)
        return cast(Callable, getattr(module, self._func))

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        return core_schema.no_info_after_validator_function(cls, handler(str))


PythonImportableObject = Annotated[
    PythonImportableObjectType,
    BeforeValidator(
        lambda x: PythonImportableObjectType(x), json_schema_input_type=str
    ),
]
