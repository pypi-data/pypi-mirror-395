import asyncio
import functools
import inspect
import signal
import threading
import time
import typing
from tqdm.asyncio import tqdm as atqdm
from contextlib import asynccontextmanager
from contextvars import ContextVar
from functools import partial, wraps
from typing import (
    TYPE_CHECKING,
    Any,
    AsyncIterator,
    Awaitable,
    Callable,
    Collection,
    Coroutine,
    Optional,
    Protocol,
    TypeVar,
    Union,
    overload,
)

import anyio
import anyio.abc
import anyio.from_thread
import anyio.to_thread
import tqdm
from loguru import logger
from typing_extensions import Literal, ParamSpec, TypeGuard

# import threading

# from prefect.logging import get_logger

T = TypeVar("T")
P = ParamSpec("P")
R = TypeVar("R")
F = TypeVar("F", bound=Callable[..., Any])
Async = Literal[True]
Sync = Literal[False]
A = TypeVar("A", Async, Sync, covariant=True)

# Global references to prevent garbage collection for `add_event_loop_shutdown_callback`
EVENT_LOOP_GC_REFS: dict[Any, Any] = {}

GLOBAL_THREAD_LIMITER: Optional[anyio.CapacityLimiter] = None

RUNNING_IN_RUN_SYNC_LOOP_FLAG = ContextVar("running_in_run_sync_loop", default=False)
RUNNING_ASYNC_FLAG = ContextVar("run_async", default=False)
BACKGROUND_TASKS: set[asyncio.Task] = set()
background_task_lock = threading.Lock()

# Thread-local storage to keep track of worker thread state
_thread_local = threading.local()


def get_thread_limiter():
    global GLOBAL_THREAD_LIMITER

    if GLOBAL_THREAD_LIMITER is None:
        GLOBAL_THREAD_LIMITER = anyio.CapacityLimiter(250)

    return GLOBAL_THREAD_LIMITER


def is_async_fn(
    func: Union[Callable[P, R], Callable[P, Awaitable[R]]],
) -> TypeGuard[Callable[P, Awaitable[R]]]:
    """
    Returns `True` if a function returns a coroutine.

    See https://github.com/microsoft/pyright/issues/2142 for an example use
    """
    while hasattr(func, "__wrapped__"):
        func = func.__wrapped__

    return inspect.iscoroutinefunction(func)


def is_async_gen_fn(func):
    """
    Returns `True` if a function is an async generator.
    """
    while hasattr(func, "__wrapped__"):
        func = func.__wrapped__

    return inspect.isasyncgenfunction(func)


def create_task(coroutine: Coroutine) -> asyncio.Task:
    """
    Replacement for asyncio.create_task that will ensure that tasks aren't
    garbage collected before they complete. Allows for "fire and forget"
    behavior in which tasks can be created and the application can move on.
    Tasks can also be awaited normally.

    See https://docs.python.org/3/library/asyncio-task.html#asyncio.create_task
    for details (and essentially this implementation)
    """

    task = asyncio.create_task(coroutine)

    # Add task to the set. This creates a strong reference.
    # Take a lock because this might be done from multiple threads.
    with background_task_lock:
        BACKGROUND_TASKS.add(task)

    # To prevent keeping references to finished tasks forever,
    # make each task remove its own reference from the set after
    # completion:
    task.add_done_callback(BACKGROUND_TASKS.discard)

    return task


def cancel_background_tasks() -> None:
    """
    Cancels all background tasks stored in BACKGROUND_TASKS.
    """
    with background_task_lock:
        tasks = list(BACKGROUND_TASKS)
    for task in tasks:
        task.cancel()


def run_async(coroutine):
    try:
        # Try to get the current event loop
        loop = asyncio.get_event_loop()
    except RuntimeError:
        # If there's no current event loop, create a new one
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    # Now we can safely run our coroutine
    return loop.run_until_complete(coroutine)


async def _async_generator_timeout(async_gen, timeout):
    try:
        while True:
            try:
                item = await asyncio.wait_for(async_gen.__anext__(), timeout)
                yield item
            except StopAsyncIteration:
                break
    except asyncio.TimeoutError:
        raise asyncio.TimeoutError(
            "Generator didn't emit a new item within the specified timeout"
        )


global_stop = threading.Event()


@overload
def async_iterator(
    func: Callable[..., AsyncIterator[T]],
) -> Callable[..., AsyncIterator[T]]: ...


@overload
def async_iterator(
    func: None = None, iteration_timeout: float | None = None
) -> Callable[[Callable[..., AsyncIterator[T]]], Callable[..., AsyncIterator[T]]]: ...


def async_iterator(
    func: Callable[..., AsyncIterator[T]] | None = None,
    iteration_timeout: float | None = None,
    use_global_stop: bool = False,
) -> (
    Callable[..., AsyncIterator[T]]
    | Callable[[Callable[..., AsyncIterator[T]]], Callable[..., AsyncIterator[T]]]
):
    def inner(
        async_iter_func: Callable[..., AsyncIterator[T]],
    ) -> Callable[..., AsyncIterator[T]]:
        @functools.wraps(async_iter_func)
        async def wrapper(*args, **kwargs) -> AsyncIterator[T]:
            stop_event = asyncio.Event() if not use_global_stop else global_stop
            loop = asyncio.get_running_loop()
            loop.add_signal_handler(signal.SIGINT, stop_event.set)
            try:
                if iteration_timeout is not None:
                    async_gen = _async_generator_timeout(
                        async_iter_func(*args, **kwargs), iteration_timeout
                    )
                else:
                    async_gen = async_iter_func(*args, **kwargs)

                async for item in async_gen:
                    if stop_event.is_set():
                        break
                    yield item
                    await asyncio.sleep(0)
            except (KeyboardInterrupt, asyncio.CancelledError):
                # logger.debug("Received interrupt signal")
                stop_event.set()
                raise
            # except* Exception as e:
            #     for exc in e.exceptions:
            #         logger.error(exc)
            finally:
                # logger.info("Cleaning up...")
                loop.remove_signal_handler(signal.SIGINT)
                return

        return wrapper

    if func is not None:
        return inner(func)

    return inner


class FunctionWithStop(Protocol):
    global_stop: threading.Event

    def __call__(self, *args: Any, **kwargs: Any) -> Any: ...


if not TYPE_CHECKING:
    setattr(async_iterator, "global_stop", global_stop)


async def handle_signals(scope: anyio.abc.CancelScope):
    async with anyio.open_signal_receiver(signal.SIGINT, signal.SIGTERM) as signals:  # type: ignore[attr-defined]
        async for signum in signals:
            logger.info(f"Received signal: {signum}")
            scope.cancel()  # This cancels th


async def _run_with(
    fn: Callable[..., Awaitable[T]],
    _idx: int,
    _stop: asyncio.Event,
    timeout: float | None = None,
    **kwargs,
) -> tuple[int, T | None | asyncio.TimeoutError]:
    if _stop.is_set():
        return _idx, None
    if timeout is None:
        return _idx, await fn(**kwargs)
    else:
        try:
            return _idx, await asyncio.wait_for(fn(**kwargs), timeout)
        except asyncio.TimeoutError as e:
            logger.warning(f"Task {_idx} timed out after {timeout} seconds")
            return _idx, e


async def map_as_completed(
    fn: Callable[..., Awaitable[T]],
    *inputs: dict[str, Any],
    name: str | None = None,
    progress: bool = True,
    return_exceptions: bool = True,
    exclude_exceptions: bool = False,
    progress_position: int = 0,
    concurrency: int | None = None,
    task_timeout: float | None = None,
) -> list[T | Exception]:
    _stop = asyncio.Event()
    output = {}
    tasks: set[asyncio.Task[tuple[int, T]]] = set()
    name = name or fn.__name__
    if concurrency:
        sem = asyncio.Semaphore(concurrency)
    else:
        sem = None

    # Create a separate error handler task outside the TaskGroup for proper cleanup
    error_handler_task = None

    try:
        # Set up a cancellation handler
        async def handle_cancellation():
            await _stop.wait()
            logger.info(f"Cancellation requested for {name} tasks")

        error_handler_task = asyncio.create_task(handle_cancellation())

        async with asyncio.TaskGroup() as tg:
            for _idx, input in enumerate(inputs):

                async def safe_run_task(_idx=_idx, input=input):
                    try:
                        return (
                            await run_with_semaphore(
                                sem,
                                _run_with(
                                    fn, _idx, _stop, timeout=task_timeout, **input
                                ),
                            )
                            if sem
                            else await _run_with(
                                fn, _idx, _stop, timeout=task_timeout, **input
                            )
                        )
                    except Exception as e:
                        if return_exceptions:
                            logger.warning(f"Task error in {name}: {str(e)}")
                            return _idx, e
                        else:
                            _stop.set()
                            raise

                task = tg.create_task(safe_run_task())
                tasks.add(task)

            for result in tqdm.tqdm(
                asyncio.as_completed(tasks),
                total=len(tasks),
                desc=name,
                disable=not progress,
                position=progress_position,
            ):
                try:
                    if _stop.is_set():
                        logger.debug(
                            f"Stopping iteration of {name} due to cancellation"
                        )
                        break
                    _idx, value = await result
                    if isinstance(value, Exception):
                        if return_exceptions:
                            logger.opt(exception=value).warning(
                                f"Task error in {name}: {str(value)}"
                            )
                            if not exclude_exceptions:
                                output[_idx] = value
                        else:
                            _stop.set()
                            raise value
                    else:
                        output[_idx] = value  # type: ignore[assignment]
                except (asyncio.CancelledError, KeyboardInterrupt) as e:
                    logger.info(f"Received cancellation in {name}: {type(e).__name__}")
                    _stop.set()
                    raise
                except Exception as e:
                    if return_exceptions:
                        logger.opt(exception=e).warning(
                            f"Task error in {name}: {str(e)}"
                        )
                        if not exclude_exceptions:
                            output[_idx] = e  # type: ignore[assignment]
                    else:
                        _stop.set()
                        raise e

    except (asyncio.CancelledError, KeyboardInterrupt):
        # Handle cancellation outside the loop
        logger.info(f"Cancelling all tasks in {name}")
        _stop.set()  # Ensure stop flag is set
        # Let the finally block handle cleanup
        raise

    except Exception as e:
        # Handle other top-level exceptions
        logger.error(f"Error in {name}: {str(e)}")
        _stop.set()
        raise

    finally:
        # Clean up the error handler task
        if error_handler_task and not error_handler_task.done():
            error_handler_task.cancel()
            try:
                # Give it a moment to clean up
                await asyncio.wait_for(error_handler_task, 0.1)
            except (asyncio.CancelledError, asyncio.TimeoutError):
                pass

        # Ensure stop event is set for any in-flight tasks
        _stop.set()

    # Return the sorted results
    return list(dict(sorted(output.items(), key=lambda x: x[0])).values())


async def map_as_completed_dict(
    fn: Callable[..., Awaitable[T]],
    inputs: dict[Any, dict[str, Any]],
    name: str | None = None,
    progress: bool = True,
    return_exceptions: bool = True,
    exclude_exceptions: bool = False,
    progress_position: int = 0,
    concurrency: int | None = None,
    task_timeout: float | None = None,
) -> dict[Any, T]:
    """
    Executes an async function `fn` concurrently using a dictionary of inputs.

    Each key in `inputs` identifies a task, and its value is a dictionary of keyword arguments
    that will be passed to `fn`. Results are returned as a dictionary mapping each key to its result.

    Example:
        inputs = {
            'user_1': {'user_id': 1},
            'user_2': {'user_id': 2},
        }
        results = await map_as_completed_dict(fetch_user_data, inputs)
        # results might be: {'user_1': user_data_1, 'user_2': user_data_2}
    """
    _stop = asyncio.Event()
    output: dict[Any, T] = {}
    tasks: list[asyncio.Task[tuple[Any, T]]] = []
    name = name or fn.__name__
    if concurrency:
        sem = asyncio.Semaphore(concurrency)
    else:
        sem = None

    async def run_task(
        key: Any, params: dict[str, Any], timeout: float | None = None
    ) -> tuple[Any, T | None | asyncio.TimeoutError]:
        if _stop.is_set():
            return key, None  # or consider raising CancelledError
        if timeout is None:
            return key, await fn(**params)
        else:
            try:
                return key, await asyncio.wait_for(fn(**params), timeout)
            except asyncio.TimeoutError as e:
                logger.warning(f"Task {key} timed out after {timeout} seconds")
                return key, e

    async with asyncio.TaskGroup() as tg:
        for key, params in inputs.items():

            async def safe_run_task(key=key, params=params):
                try:
                    return (
                        await run_with_semaphore(
                            sem, run_task(key, params, timeout=task_timeout)
                        )
                        if sem
                        else await run_task(key, params, timeout=task_timeout)
                    )
                except Exception as e:
                    if return_exceptions:
                        return key, e
                    else:
                        raise

            tasks.append(tg.create_task(safe_run_task()))

    for result in tqdm.tqdm(
        asyncio.as_completed(tasks),
        total=len(tasks),
        desc=name,
        disable=not progress,
        position=progress_position,
    ):
        try:
            key, value = await result
            if isinstance(value, Exception):
                if return_exceptions:
                    logger.opt(exception=value).warning(
                        f"Task error in {name}: {str(value)}"
                    )
                    if not exclude_exceptions:
                        output[key] = value
                else:
                    _stop.set()
                    raise value
            else:
                output[key] = value
            output[key] = value
        except (asyncio.CancelledError, KeyboardInterrupt):
            _stop.set()
            raise
        except Exception as e:
            if return_exceptions:
                logger.opt(exception=e).warning(f"Task error in {name}: {str(e)}")
                if not exclude_exceptions:
                    output[key] = e  # type: ignore[assignment]
            else:
                raise e
    # sort final outputs by original key order
    return dict(sorted(output.items(), key=lambda x: list(inputs.keys()).index(x[0])))


async def run_with_semaphore(
    semaphore: asyncio.Semaphore | None,
    coro: typing.Coroutine,
):
    if semaphore is None:
        return await coro
    async with semaphore:
        return await coro


def retry_async(
    retries: int = 3,
    delay: float = 1.0,
    backoff_factor: float = 2.0,
    exceptions: tuple = (Exception,),
):
    """
    Decorator that implements retry logic for async functions with exponential backoff.

    Args:
        retries: Maximum number of retries
        delay: Initial delay between retries in seconds
        backoff_factor: Multiplier for delay after each retry
        exceptions: Tuple of exceptions to catch and retry
    """

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            last_exception: BaseException | None = None
            current_delay = delay

            for attempt in range(retries + 1):
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt == retries:
                        raise
                    await asyncio.sleep(current_delay)
                    current_delay *= backoff_factor

            if last_exception is not None:
                raise last_exception
            raise RuntimeError("retry_async exhausted without raising an exception")

        return wrapper

    return decorator


async def gather_with_concurrency(n: int, *tasks) -> list[T]:
    """
    Run coroutines with a concurrency limit.

    Args:
        n: Maximum number of concurrent tasks
        tasks: Coroutines to run
    """
    semaphore = asyncio.Semaphore(n)

    results = await asyncio.gather(
        *(run_with_semaphore(semaphore, task) for task in tasks)
    )
    return list(results)


@asynccontextmanager
async def timeout_scope(timeout: float, cleanup: Optional[Callable] = None):
    """
    Async context manager that enforces a timeout and allows for cleanup.

    Args:
        timeout: Maximum time in seconds
        cleanup: Optional coroutine to run on timeout
    """
    try:
        async with asyncio.timeout(timeout):
            yield
    except asyncio.TimeoutError:
        if cleanup:
            await cleanup()
        raise


def ensure_async(func: Callable[..., R]) -> Callable[..., Awaitable[R]]:
    """
    Wraps a synchronous function so that it can be awaited.

    If the function is already async, it is returned unchanged.
    """
    if asyncio.iscoroutinefunction(func):
        return func

    @wraps(func)
    async def async_wrapper(*args, **kwargs) -> R:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, partial(func, *args, **kwargs))

    return async_wrapper


class AsyncBatcher(typing.Generic[T]):
    """
    # AsyncBatcher

    The `AsyncBatcher` class provides a mechanism to efficiently batch asynchronous operations and process them together when either:
    1. The batch size threshold is reached
    2. A timeout period has elapsed
    3. The context manager is exited

    ## Installation

    This class requires Python 3.7+ with `asyncio` support.

    ## Basic Usage

    ```python
    import asyncio
    from typing import Collection, List

    async def process_batch(items: Collection[str]) -> None:
        print(f"Processing batch of {len(items)}: {items}")

    async def main():
        # Create a batcher that processes 5 items at a time with a 2-second timeout
        async with AsyncBatcher(
            batch_size=5,
            processor=process_batch,
            timeout=2.0
        ) as batcher:
            # Add items individually
            for i in range(12):
                await batcher.add(f"item-{i}")
                await asyncio.sleep(0.5)

            # Items will be processed in batches of 5, or when 2 seconds elapsed
            # Any remaining items are processed on context exit

    asyncio.run(main())
    ```

    ## Constructor Parameters

    - **batch_size** (*int*): Maximum number of items to collect before triggering batch processing
    - **processor** (*Callable[[Collection[T]], Awaitable[None]]*): Async function that processes a collection of items
    - **timeout** (*Optional[float]*): Maximum time (in seconds) to wait before processing a non-empty batch even if batch_size hasn't been reached. If `None`, batches will only be processed when batch_size is reached or on context exit.

    ## Methods

    ### `async add(item: T) -> None`

    Adds a single item to the current batch. If adding this item causes the batch size to reach the `batch_size` threshold, the batch will be automatically processed.

    ```python
    await batcher.add("new_item")
    ```

    ### Context Manager Support

    `AsyncBatcher` is designed to be used as an async context manager, which ensures proper cleanup and processing of any remaining items:

    ```python
    async with AsyncBatcher(batch_size, processor, timeout) as batcher:
        await batcher.add(item1)
        await batcher.add(item2)
        # ...
    # Any remaining items are processed when exiting the context
    ```

    ## Internal Operations

    - The batcher maintains an internal lock to ensure thread safety during batch management
    - When timeout is specified, a background task monitors the elapsed time since the last batch processing
    - On context exit, any remaining items in the batch are processed and the timeout task is cleaned up

    ## Example: Processing API Requests

    ```python
    async def process_api_requests(requests: Collection[dict]) -> None:
        async with aiohttp.ClientSession() as session:
            tasks = [session.post("https://api.example.com/batch", json=req) for req in requests]
            await asyncio.gather(*tasks)

    async def main():
        async with AsyncBatcher(
            batch_size=10,
            processor=process_api_requests,
            timeout=5.0
        ) as batcher:
            # Add API requests as they come in
            while more_requests_coming:
                request = await get_next_request()
                await batcher.add(request)
    ```

    ## Best Practices

    1. Choose an appropriate batch size for your specific workload
    2. Set a reasonable timeout based on your latency requirements
    3. Always use the async context manager to ensure proper cleanup
    4. Make sure your processor function properly handles the batch collection
    5. The processor is responsible for handling any errors within the batch items
    """

    def __init__(
        self,
        batch_size: int,
        processor: Callable[[Collection[T]], Awaitable[None]],
        timeout: Optional[float] = None,
    ):
        self.batch_size = batch_size
        self.processor = processor
        self.timeout = timeout
        self.batch: list[T] = []
        self.last_process_time = time.time()
        self._stop_event = asyncio.Event()
        self._timeout_task: Optional[asyncio.Task] = None
        self._lock = asyncio.Lock()

        # Start timeout checker if timeout is specified
        if timeout is not None:
            self._timeout_task = asyncio.create_task(self._check_timeout())

    async def add(self, item: T) -> None:
        """Add an item to the batch and process if necessary."""
        async with self._lock:
            self.batch.append(item)

            if len(self.batch) >= self.batch_size:
                await self._process_internal()

    async def _process_internal(self) -> None:
        """Internal method to process the current batch."""
        if not self.batch:
            return

        items_to_process = self.batch[:]
        self.batch = []
        self.last_process_time = time.time()

        await self.processor(items_to_process)

    async def _check_timeout(self) -> None:
        """Background task to check for timeouts."""
        while not self._stop_event.is_set():
            if self.timeout is None:
                return

            try:
                await asyncio.wait_for(self._stop_event.wait(), timeout=self.timeout)
            except asyncio.TimeoutError:
                async with self._lock:
                    current_time = time.time()
                    if (
                        self.batch
                        and current_time - self.last_process_time >= self.timeout
                    ):
                        await self._process_internal()
                continue

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Process remaining items and cleanup on exit."""
        self._stop_event.set()

        if self._timeout_task:
            await self._timeout_task

        async with self._lock:
            await self._process_internal()


async def periodic(
    interval: float,
    func: Callable[[], Awaitable[None]],
    max_delay: Optional[float] = None,
) -> AsyncIterator[float]:
    """
    Runs a coroutine periodically and yields the actual time between runs.

    Args:
        interval: Desired interval between runs in seconds
        func: Coroutine to run
        max_delay: Maximum acceptable delay before skipping an iteration
    """
    last_run = time.time()

    while True:
        now = time.time()
        elapsed = now - last_run

        if max_delay is None or elapsed <= max_delay:
            await func()

        target_next = last_run + interval
        delay = max(0, target_next - time.time())

        if delay > 0:
            await asyncio.sleep(delay)

        actual_interval = time.time() - last_run
        last_run = time.time()

        yield actual_interval


class AsyncRateLimiter:
    """
    # AsyncRateLimiter

    The `AsyncRateLimiter` class provides rate limiting for asynchronous operations using the token bucket algorithm. It controls the rate at which operations can be performed while allowing for occasional bursts of activity.

    ## Installation

    This class requires Python 3.7+ with `asyncio` support.

    ## Basic Usage

    ```python
    import asyncio
    import time

    async def main():
        # Create a rate limiter with 2 operations per second and a burst capacity of 5
        limiter = AsyncRateLimiter(rate=2.0, burst=5)

        # Use the rate limiter to control operation frequency
        for i in range(10):
            await limiter.acquire()  # This will wait if necessary to maintain the rate limit
            print(f"Operation {i} at {time.time()}")

        # Operations will be spaced out to maintain approximately 2 per second

    asyncio.run(main())
    ```

    ## Constructor Parameters

    - **rate** (*float*): Maximum sustained rate of operations per second
    - **burst** (*int, default=1*): Maximum number of operations that can be performed immediately in a burst before rate limiting takes effect

    ## Methods

    ### `async acquire()`

    Acquires permission to perform an operation. If the rate limit would be exceeded, this method will wait until permission can be granted according to the configured rate.

    ```python
    await rate_limiter.acquire()
    # Perform your rate-limited operation here
    ```

    This method:
    1. Updates the token count based on elapsed time
    2. If sufficient tokens are available, decrements the token count and returns immediately
    3. If insufficient tokens are available, waits until the operation can be performed according to the rate limit

    ## How the Token Bucket Algorithm Works

    1. The limiter maintains a bucket of "tokens" (initially filled to the burst capacity)
    2. Tokens regenerate at the specified rate per second
    3. Each operation consumes one token
    4. If no tokens are available, the operation must wait
    5. The bucket can never contain more tokens than the burst capacity

    ## Example: Rate-Limited API Client

    ```python
    import aiohttp

    async def rate_limited_api_client():
        # Allow 5 requests per second with bursts of up to 10
        limiter = AsyncRateLimiter(rate=5.0, burst=10)

        async with aiohttp.ClientSession() as session:
            for i in range(100):
                await limiter.acquire()  # Wait if we're exceeding our rate limit
                async with session.get(f"https://api.example.com/resource/{i}") as response:
                    data = await response.json()
                    process_data(data)
    ```

    ## Example: Combining with AsyncBatcher

    ```python
    async def process_batch(items):
        print(f"Processing batch of {len(items)} items")

    async def main():
        # Limit to 2 batches per second
        limiter = AsyncRateLimiter(rate=2.0, burst=1)

        # Process items in batches of 5
        async with AsyncBatcher(batch_size=5, processor=process_batch) as batcher:
            for i in range(50):
                # Add items at a controlled rate
                await limiter.acquire()
                await batcher.add(f"item-{i}")
    ```

    ## Best Practices

    1. Choose an appropriate rate based on the resource constraints (e.g., API rate limits)
    2. Set the burst capacity based on how many operations can safely be performed in quick succession
    3. Always await the `acquire()` method before performing the rate-limited operation
    4. Consider using a rate limiter per resource or endpoint when dealing with multiple rate-limited resources
    5. For very low rates (less than 1 per second), ensure your application can handle the waiting periods
    """

    def __init__(self, rate: float, burst: int = 1):
        self.rate = rate  # tokens per second
        self.burst = burst
        self.tokens: float = float(burst)
        self.last_update = time.time()
        self._lock = asyncio.Lock()

    async def acquire(self):
        async with self._lock:
            now = time.time()
            elapsed = now - self.last_update
            self.tokens = min(self.burst, self.tokens + elapsed * self.rate)
            self.last_update = now

            if self.tokens < 1:
                wait_time = (1 - self.tokens) / self.rate
                await asyncio.sleep(wait_time)
                self.tokens = 0
                self.last_update = time.time()
            else:
                self.tokens -= 1


async def gather_progress(
    *fs,
    loop=None,
    timeout=None,
    total=None,
    return_exceptions: bool = False,
    **tqdm_kwargs,
):
    """
    Wrapper for `asyncio.gather`.
    """

    async def wrap_awaitable(i, f):
        try:
            return i, await f
        except Exception as e:
            if return_exceptions:
                return i, e
            else:
                raise e

    ifs = [wrap_awaitable(i, f) for i, f in enumerate(fs)]
    res = [
        await f
        for f in atqdm.as_completed(
            ifs, loop=loop, timeout=timeout, total=total, **tqdm_kwargs
        )
    ]
    return [i for _, i in sorted(res)]
