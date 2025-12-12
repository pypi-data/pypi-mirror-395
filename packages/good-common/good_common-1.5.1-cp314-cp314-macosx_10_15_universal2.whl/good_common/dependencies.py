"""
Dependencies module for good_common.
Provides base classes for dependency injection with fast_depends.
"""

import copy
import typing
import warnings
from typing import cast
from fast_depends.library import CustomField
from loguru import logger
import inspect

warnings.warn(
    "The good_common.dependencies module is deprecated and will be removed in a future version. "
    "Please use the fast_depends library directly.",
    DeprecationWarning,
    stacklevel=2,
)

T = typing.TypeVar("T")


def _get_generic_type(cls):
    """Extract the generic type parameter from BaseProvider[T] or AsyncBaseProvider[T]"""
    # Check if __orig_bases__ exists (Python 3.7+)
    if hasattr(cls, "__orig_bases__"):
        for base in cls.__orig_bases__:
            origin = typing.get_origin(base)
            # Check if this is our generic base class
            if origin is BaseProvider or (origin and issubclass(origin, BaseProvider)):
                args = typing.get_args(base)
                if args:
                    return args[0]
            elif origin is AsyncBaseProvider or (
                origin and issubclass(origin, AsyncBaseProvider)
            ):
                args = typing.get_args(base)
                if args:
                    return args[0]

    # Fallback to old behavior for backward compatibility
    # This handles the case where the class inherits from both BaseProvider[T] and T
    if len(cls.__bases__) > 1:
        for base in cls.__bases__:
            # Skip the provider base classes
            if not (
                base is BaseProvider
                or base is AsyncBaseProvider
                or (
                    hasattr(base, "__origin__")
                    and typing.get_origin(base) in (BaseProvider, AsyncBaseProvider)
                )
            ):
                return base

    return None


class BaseProvider(CustomField, typing.Generic[T]):
    __override_class__: typing.ClassVar = None

    @classmethod
    def provide(cls, *args, **kwargs) -> T:
        _kwargs = kwargs.copy()
        _target_cls = cls.__override_class__ or _get_generic_type(cls)
        if _target_cls is None:
            raise TypeError(
                f"Could not determine target class for {cls.__name__}. "
                "Make sure to inherit from BaseProvider[YourClass]."
            )

        _args = inspect.getfullargspec(_target_cls.__init__)

        if not _args.varkw:
            _remove_args = set()
            for k, v in kwargs.items():
                if k not in _args.args:
                    # logger.debug(f"Removing {k}")
                    _remove_args.add(k)
                    _kwargs.pop(k)

            if _remove_args:
                logger.debug(f"Removing {len(_remove_args)} args: {_remove_args}")

        kwargs = _kwargs

        if cls.__override_class__ is not None:
            return cast(T, cls.__override_class__(*args, **kwargs))
        else:
            return cast(T, _target_cls(*args, **kwargs))

    def __init__(self, *args, _debug: bool = False, **kwargs):
        super().__init__(cast=False)
        self._args = args
        self._kwargs = kwargs
        self._debug = _debug
        self._warning_shown = False

    def initializer(
        self,
        cls_args: tuple[typing.Any, ...],
        cls_kwargs: dict[str, typing.Any],
        fn_kwargs: dict[str, typing.Any],
    ):
        return cls_args, (cls_kwargs or {}) | (fn_kwargs or {})

    def use(self, /, **kwargs: dict[str, typing.Any]):
        if self._debug:
            logger.debug(f"Using {self.__class__.__name__}: {kwargs}")

        # Check if using old pattern and show deprecation warning
        if not self._warning_shown and self.param_name and self._is_used_as_default():
            self._show_deprecation_warning()
            self._warning_shown = True

        kwargs = super().use(**kwargs)
        if self.param_name:
            _args, _kwargs = self.initializer(
                cls_args=copy.copy(self._args),
                cls_kwargs=copy.copy(self._kwargs),
                fn_kwargs=kwargs,
            )
            kwargs[self.param_name] = self.provide(*_args, **_kwargs)  # type: ignore
        return kwargs

    def get(self, **kwargs) -> T:
        self.param_name = "_default"
        return self.use(**kwargs).get(self.param_name)  # type: ignore

    def _is_used_as_default(self) -> bool:
        """Check if this provider is being used as a function default value"""
        # Inspect the call stack to find the injected function
        frame = inspect.currentframe()
        try:
            # Walk up the stack to find the decorated function
            while frame:
                frame_locals = frame.f_locals

                # Look for function objects that might contain this provider as a default
                for name, obj in frame_locals.items():
                    if callable(obj):
                        # Check both the function and its wrapped version (for @inject)
                        funcs_to_check = [obj]
                        if hasattr(obj, "__wrapped__"):
                            funcs_to_check.append(obj.__wrapped__)

                        for func in funcs_to_check:
                            if hasattr(func, "__defaults__") and func.__defaults__:
                                if self in func.__defaults__:
                                    # Check if this function parameter uses Annotated
                                    sig = inspect.signature(func)
                                    for param_name, param in sig.parameters.items():
                                        if param.default is self:
                                            # Check if the annotation is Annotated
                                            if (
                                                typing.get_origin(param.annotation)
                                                is not typing.Annotated
                                            ):
                                                return True

                frame = frame.f_back
        finally:
            del frame

        return False

    def _show_deprecation_warning(self):
        """Show deprecation warning with migration guide"""
        target_type = _get_generic_type(self.__class__)
        type_name = target_type.__name__ if target_type else "YourType"

        warnings.warn(
            f"Using {self.__class__.__name__} as a default parameter value is deprecated and will be removed in a future version.\n"
            f"Please use the Annotated pattern instead:\n"
            f"  Old: func(param: {type_name} = {self.__class__.__name__}(...))\n"
            f"  New: func(param: Annotated[{type_name}, {self.__class__.__name__}(...)])",
            DeprecationWarning,
            stacklevel=6,  # Adjusted to show the user's code
        )


class AsyncBaseProvider(CustomField, typing.Generic[T]):
    __override_class__: typing.ClassVar = None

    async def get(self, **kwargs) -> T:
        self.param_name = "_default"
        return (await self.use(**kwargs)).get(self.param_name)  # type: ignore[return-value]

    @classmethod
    async def provide(cls, *args, **kwargs) -> T:
        if cls.__override_class__ is not None:
            return cast(T, cls.__override_class__(*args, **kwargs))
        else:
            _target_cls = _get_generic_type(cls)
            if _target_cls is None:
                raise TypeError(
                    f"Could not determine target class for {cls.__name__}. "
                    "Make sure to inherit from AsyncBaseProvider[YourClass]."
                )
            return cast(T, _target_cls(*args, **kwargs))

    def __init__(self, *args, _debug: bool = False, **kwargs):
        super().__init__(cast=False)
        self._args = args
        self._kwargs = kwargs
        self._debug = _debug
        self._warning_shown = False

    def initializer(
        self,
        cls_args: tuple[typing.Any, ...],
        cls_kwargs: dict[str, typing.Any],
        fn_kwargs: dict[str, typing.Any],
    ):
        return cls_args, (cls_kwargs or {}) | (fn_kwargs or {})

    async def use(self, /, **kwargs: dict[str, typing.Any]) -> dict[str, typing.Any]:  # type: ignore[override]
        if self._debug:
            logger.debug(f"Using {self.__class__.__name__}: {kwargs}")

        # Check if using old pattern and show deprecation warning
        if not self._warning_shown and self.param_name and self._is_used_as_default():
            self._show_deprecation_warning()
            self._warning_shown = True

        kwargs = super().use(**kwargs)
        if self.param_name:
            _args, _kwargs = self.initializer(
                cls_args=copy.copy(self._args),
                cls_kwargs=copy.copy(self._kwargs),
                fn_kwargs=kwargs,
            )
            kwargs[self.param_name] = await self.provide(*_args, **_kwargs)  # type: ignore

            await self.on_initialize(
                kwargs[self.param_name],
                **{k: v for k, v in _kwargs.items() if k != self.param_name},
            )
        return kwargs

    async def on_initialize(self, instance, **kwargs):
        pass

    def _is_used_as_default(self) -> bool:
        """Check if this provider is being used as a function default value"""
        # Inspect the call stack to find the injected function
        frame = inspect.currentframe()
        try:
            # Walk up the stack to find the decorated function
            while frame:
                frame_locals = frame.f_locals

                # Look for function objects that might contain this provider as a default
                for name, obj in frame_locals.items():
                    if callable(obj):
                        # Check both the function and its wrapped version (for @inject)
                        funcs_to_check = [obj]
                        if hasattr(obj, "__wrapped__"):
                            funcs_to_check.append(obj.__wrapped__)

                        for func in funcs_to_check:
                            if hasattr(func, "__defaults__") and func.__defaults__:
                                if self in func.__defaults__:
                                    # Check if this function parameter uses Annotated
                                    sig = inspect.signature(func)
                                    for param_name, param in sig.parameters.items():
                                        if param.default is self:
                                            # Check if the annotation is Annotated
                                            if (
                                                typing.get_origin(param.annotation)
                                                is not typing.Annotated
                                            ):
                                                return True

                frame = frame.f_back
        finally:
            del frame

        return False

    def _show_deprecation_warning(self):
        """Show deprecation warning with migration guide"""
        target_type = _get_generic_type(self.__class__)
        type_name = target_type.__name__ if target_type else "YourType"

        warnings.warn(
            f"Using {self.__class__.__name__} as a default parameter value is deprecated and will be removed in a future version.\n"
            f"Please use the Annotated pattern instead:\n"
            f"  Old: func(param: {type_name} = {self.__class__.__name__}(...))\n"
            f"  New: func(param: Annotated[{type_name}, {self.__class__.__name__}(...)])",
            DeprecationWarning,
            stacklevel=6,  # Adjusted to show the user's code
        )
