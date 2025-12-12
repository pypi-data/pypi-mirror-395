from __future__ import annotations
import asyncio
from concurrent.futures import ThreadPoolExecutor, as_completed
import anyio.to_thread
from fast_depends import inject
from fast_depends.core import CallModel
from fast_depends.dependencies import model
from loguru import logger
from abc import ABC, abstractmethod
import collections
import functools
import inspect
import tqdm
import tqdm.asyncio as tqdm_asyncio
import typing
import anyio
from functools import partial

# from functools import up
from copy import deepcopy
from result import Ok, Err, Result


def is_inject_decorated(fn):
    return (
        hasattr(fn, "__closure__")
        and len((fn.__closure__ or [])) > 1
        and isinstance(fn.__closure__[1].cell_contents, CallModel)
    )


class Output:
    def __init__(self):
        self._data = {}
        self._types = {}
        self._locked = False

    def register(self, name: str, data_type: str):
        self._types[name] = data_type

    def lock(self):
        self._locked = True

    def copy(self) -> typing.Self:
        return deepcopy(self)

    def __setattr__(self, name: str, value: typing.Any):
        if name in ["_data", "_types", "_locked"]:
            super().__setattr__(name, value)
            return

        if self._locked:
            raise AttributeError("Output is locked. Cannot add new attributes")

        if name in self._types:
            expected_type = self._types[name]
            if not self._check_type(value, expected_type):
                raise TypeError(f"Value for {name} must be of type {expected_type}")

        self._data[name] = value

    def __getattr__(self, name: str) -> typing.Any:
        if name == "_data":
            raise AttributeError()
        if name in self._data:
            return self._data[name]
        raise AttributeError(f"{name} not found")

    def _check_type(self, value: typing.Any, expected_type: str) -> bool:
        origin_type = typing.get_origin(expected_type)
        type_args = typing.get_args(expected_type)

        if isinstance(origin_type, type) and origin_type in [list, set, tuple]:
            if not isinstance(value, origin_type):
                return False
            try:
                if hasattr(value, "__iter__"):
                    return all(self._check_type(item, type_args[0]) for item in value)
                else:
                    return False
            except (TypeError, AttributeError):
                return False

        if origin_type is dict:
            if not isinstance(value, dict):
                return False
            key_type, val_type = type_args
            return all(
                self._check_type(k, key_type) and self._check_type(v, val_type)
                for k, v in value.items()
            )

        if origin_type is typing.Union:
            return any(self._check_type(value, arg) for arg in type_args)

        return type(value).__name__ == expected_type

    def __repr__(self):
        _key_types = ", ".join(f"{k}: {v}" for k, v in self._types.items())
        return f"{self.__class__.__name__}({_key_types})"

    def as_dict(self) -> dict[str, typing.Any]:
        return self._data.copy()


class PipelineResult:
    def __init__(
        self,
        sync_generator: typing.Generator[Result[Output, Exception], None, None]
        | None = None,
        async_generator: typing.AsyncGenerator[Result[Output, Exception], None]
        | None = None,
    ):
        self._sync_generator = sync_generator
        self._async_generator = async_generator

    def __iter__(self) -> typing.Iterator[Result[Output, Exception]]:
        if self._sync_generator:
            return iter(self._sync_generator)
        else:
            raise TypeError("Cannot use __iter__ on an async pipeline result")

    async def __aiter__(self) -> typing.AsyncIterator[Result[Output, Exception]]:
        if self._async_generator:
            async for result in self._async_generator:
                yield result
        elif self._sync_generator:
            # Wrap the synchronous generator in an async generator
            for result in self._sync_generator:
                yield result
        else:
            raise TypeError("No generator available for iteration")

    def __repr__(self) -> str:
        return f"PipelineResult(sync_generator={self._sync_generator}, async_generator={self._async_generator})"


_ANONYMOUS = "_anonymous"

T = typing.TypeVar("T", bound=typing.Callable, covariant=True)


# @typing.runtime_checkable
class IComponent(typing.Protocol[T]):
    @property
    def __name__(self) -> str: ...

    def __call__(self, *args, **kwargs) -> typing.Any: ...


class AbstractComponent(ABC, IComponent):
    @property
    def __name__(self) -> str:
        return str(self.__class__.__name__)

    @abstractmethod
    def __call__(self, *args, **kwargs) -> typing.Any:
        pass


class Attribute:
    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self) -> str:
        return f"Attribute({self.name})"


class Pipeline:
    def __init__(self, *fns: IComponent, debug: bool = False, **defaults):
        self._defaults = defaults
        self._pipeline: list[IComponent] = []
        self._steps = 0
        self._slot_names: list[str] = []
        self._slots: dict[str, typing.Any] = {}
        self._output = Output()
        self._func_metadata: dict[IComponent, typing.Any] = {}
        self._debug = debug

        for fn in fns:
            self.apply(fn)

    def apply(self, fn: IComponent):
        if not is_inject_decorated(fn):
            fn = inject(fn)
        func_idx = self._register_function(fn)
        assert func_idx == self._steps
        self._steps += 1

    def _register_function(self, fn: IComponent) -> int:
        if fn in self._func_metadata:
            raise ValueError(f"Function {fn.__name__} already registered")
        self._pipeline.append(fn)
        func_idx = len(self._pipeline) - 1
        _type_reference = collections.defaultdict(set)

        input_spec = self._get_function_input_spec(fn)

        if input_spec.get(_ANONYMOUS) is not None:
            logger.warning(f"Anonymous type found in function {fn.__name__} parameter ")

        for name, _type in input_spec.items():
            _type_reference[_type].add(name)
            self._add_slot(name, _type)

        output_spec = self._get_function_return_spec(fn)

        if output_spec.get(_ANONYMOUS) is not None:
            _return_type = output_spec.get(_ANONYMOUS)
            if _return_type not in _type_reference:
                raise ValueError(
                    f"Anonymous type {_return_type} not "
                    f"found in function {fn.__name__} parameters. "
                    f"Please specify a named return type"
                )
            if len(_type_reference[_return_type]) > 1:
                raise ValueError(f"Return type {_return_type} is ambiguous")
            _name = _type_reference[_return_type].pop()
            output_spec[_name] = output_spec.pop(_ANONYMOUS)

        for name, _type in output_spec.items():
            self._add_slot(str(name), _type)

        self._func_metadata[fn] = input_spec, output_spec

        return func_idx

    def _add_slot(self, name: str, _type: type | str):
        if isinstance(name, typing.ForwardRef):
            name = name.__forward_arg__

        if isinstance(_type, str):
            _data_type_str = _type
        elif isinstance(_type, type):
            _data_type_str = _type.__name__

        if name in self._slots:
            if self._slots[name] != _data_type_str:
                logger.debug((self._slots[name], _data_type_str))
                raise ValueError(
                    f"Slot {name} already exists with type {self._slots[name]}"
                )

        self._slot_names.append(name)
        self._slots[name] = _data_type_str
        self._output.register(name, _data_type_str)
        if name in self._defaults:
            setattr(self._output, str(name), self._defaults[name])

    def _get_function_input_spec(self, fn: IComponent):
        if hasattr(fn, "__wrapped__"):
            sig = inspect.signature(getattr(fn, "__wrapped__"))
        else:
            sig = inspect.signature(fn)

        input_spec = {}
        # sig = inspect.signature(_fn)

        for name, _type in sig.parameters.items():
            if _type.default is not inspect.Parameter.empty:
                if hasattr(model, "Depends") and isinstance(
                    _type.default, model.Depends
                ):
                    continue
                continue
            if typing.get_origin(_type.annotation) is typing.Annotated:
                _data_type, _annotation = typing.get_args(_type.annotation)
            else:
                _data_type = _type.annotation
                _annotation = None
            input_spec[name] = _data_type

        return input_spec

    def _get_function_return_spec(self, fn: IComponent):
        if hasattr(fn, "__wrapped__"):
            fn = getattr(fn, "__wrapped__")

        spec = {}

        if isinstance(fn, AbstractComponent):
            annotation = typing.get_type_hints(
                fn.__class__.__call__, include_extras=True
            )["return"]
        else:
            annotation = typing.get_type_hints(fn, include_extras=True)["return"]

        if typing.get_origin(annotation) is typing.Annotated:
            _type, annotation = typing.get_args(annotation)
        else:
            _type, annotation = annotation, None
        if typing.get_origin(_type) in (typing.Tuple, tuple):
            for _arg in typing.get_args(_type):
                _type, annotation = typing.get_args(_arg)
                if not annotation:
                    if _ANONYMOUS not in spec:
                        spec[_ANONYMOUS] = _type
                    else:
                        raise ValueError(f"Cannot have multiple {_ANONYMOUS} types")
                else:
                    spec[annotation] = _type
        else:
            spec[annotation if annotation is not None else _ANONYMOUS] = _type

        return {
            k if not isinstance(k, typing.ForwardRef) else k.__forward_arg__: v.__name__
            if not isinstance(v, str)
            else v
            for k, v in spec.items()
        }

    async def run(self, **inputs):
        output = self._output.copy()

        output._data = inputs

        for fn in self._pipeline:
            input_spec, output_spec = self._func_metadata[fn]
            kwargs = {}
            for name, _type in input_spec.items():
                if name in inputs:
                    kwargs[name] = deepcopy(inputs[name])
                elif hasattr(output, name):
                    kwargs[name] = deepcopy(getattr(output, name))
                else:
                    raise ValueError(f"Missing input {name} for function {fn.__name__}")

            if self._debug:
                logger.debug(f"Running {fn.__name__} with inputs {kwargs}")

            if inspect.iscoroutinefunction(fn):
                fn_output = await fn(**kwargs)
            else:
                fn_output = await anyio.to_thread.run_sync(partial(fn, **kwargs))

            if not isinstance(fn_output, tuple):
                assert len(output_spec) == 1
                fn_output = (fn_output,)

            for _output, _name in zip(fn_output, output_spec.keys()):
                setattr(output, str(_name), _output)

        output.lock()

        return output

    def run_sync(self, **inputs):
        output = self._output.copy()

        output._data = inputs

        for fn in self._pipeline:
            input_spec, output_spec = self._func_metadata[fn]
            kwargs = {}
            for name, _type in input_spec.items():
                if name in inputs:
                    kwargs[name] = deepcopy(inputs[name])
                elif hasattr(output, name):
                    kwargs[name] = deepcopy(getattr(output, name))
                else:
                    raise ValueError(f"Missing input {name} for function {fn.__name__}")

            if self._debug:
                logger.debug(f"Running {fn.__name__} with inputs {kwargs}")

            if inspect.iscoroutinefunction(fn):
                fn_output = asyncio.run(fn(**kwargs))
            else:
                fn_output = fn(**kwargs)

            if not isinstance(fn_output, tuple):
                assert len(output_spec) == 1
                fn_output = (fn_output,)

            for _output, _name in zip(fn_output, output_spec.keys()):
                setattr(output, str(_name), _output)

        output.lock()

        return output

    async def __call__(self, *args, **inputs):
        if len(args) > 0:
            for ix in range(len(args)):
                assert self._slots[self._slot_names[ix]] == type(args[ix]).__name__
                if self._slot_names[ix] in inputs:
                    raise ValueError(
                        f"Slot {self._slot_names[ix]} already specified in inputs"
                    )
                inputs[self._slot_names[ix]] = args[ix]

        return await self.run(**inputs)

    def copy(self) -> typing.Self:
        pl = self.__class__(**self._defaults)
        pl._pipeline = self._pipeline.copy()
        pl._steps = self._steps
        pl._slot_names = self._slot_names.copy()
        pl._slots = self._slots.copy()
        pl._output = self._output
        pl._func_metadata = self._func_metadata.copy()
        return pl

    async def async_execute(
        self,
        *inputs: dict[str, typing.Any],
        max_workers: int = 10,
        preserve_order: bool = True,
        display_progress: bool = False,
    ) -> typing.AsyncGenerator[Result[Output, Exception], None]:
        # This is the async execution logic
        with ThreadPoolExecutor(max_workers=max_workers) as _executor:
            futures = []
            for input in inputs:
                pl = self.copy()
                future = asyncio.ensure_future(pl(**input))
                futures.append(future)

            if preserve_order:
                for future in tqdm_asyncio.tqdm(
                    futures, disable=not display_progress, total=len(futures)
                ):
                    try:
                        r = await future
                        yield Ok(r)
                    except Exception as e:
                        yield Err(e)
            else:
                for future in tqdm_asyncio.tqdm.as_completed(futures):
                    try:
                        r = await future
                        yield Ok(r)
                    except Exception as e:
                        yield Err(e)

    def sync_execute(
        self,
        *inputs: dict[str, typing.Any],
        max_workers: int = 10,
        preserve_order: bool = True,
        display_progress: bool = False,
    ) -> typing.Generator[Result[Output, Exception], None, None]:
        # This is the sync execution logic
        with ThreadPoolExecutor(max_workers=max_workers) as _executor:
            futures = []
            for input in inputs:
                pl = self.copy()
                future = _executor.submit(pl.run_sync, **input)
                futures.append(future)

            if preserve_order:
                for future in tqdm.tqdm(
                    futures, disable=not display_progress, total=len(futures)
                ):
                    try:
                        r = future.result()
                        yield Ok(r)
                    except Exception as e:
                        yield Err(e)
            else:
                for future in tqdm.tqdm(
                    as_completed(futures),
                    disable=not display_progress,
                    total=len(futures),
                ):
                    try:
                        r = future.result()
                        yield Ok(r)
                    except Exception as e:
                        yield Err(e)

    def execute(
        self,
        *inputs: dict[str, typing.Any],
        max_workers: int = 10,
        preserve_order: bool = True,
        display_progress: bool = False,
    ) -> PipelineResult:
        # Determine if we need to run async or sync
        is_async = any(asyncio.iscoroutinefunction(fn) for fn in self._pipeline)

        if is_async:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                return PipelineResult(
                    async_generator=self.async_execute(
                        *inputs,
                        max_workers=max_workers,
                        preserve_order=preserve_order,
                        display_progress=display_progress,
                    )
                )
            else:

                async def collect_results():
                    results = []
                    async for result in self.async_execute(
                        *inputs,
                        max_workers=max_workers,
                        preserve_order=preserve_order,
                        display_progress=display_progress,
                    ):
                        results.append(result)
                    return results

                results = loop.run_until_complete(collect_results())
                logger.debug(results)
                return PipelineResult(sync_generator=(result for result in results))

        else:
            return PipelineResult(
                sync_generator=self.sync_execute(
                    *inputs,
                    max_workers=max_workers,
                    preserve_order=preserve_order,
                    display_progress=display_progress,
                )
            )

    def __repr__(self) -> str:
        _slot_types = ", ".join(f"{k}: {v}" for k, v in self._slots.items())
        return f"Pipeline({_slot_types})"


def pipeline(*fns: IComponent, **defaults):
    return Pipeline(*fns, **defaults)


def function_mapper(fn: IComponent, **mapping):
    @functools.wraps(fn)
    def _wrapper(**kwargs):
        for key, value in mapping.items():
            if key in kwargs:
                kwargs[value] = kwargs.pop(key)
        return fn(**kwargs)

    return _wrapper
