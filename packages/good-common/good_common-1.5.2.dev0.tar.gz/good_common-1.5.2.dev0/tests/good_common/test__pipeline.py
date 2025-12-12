import pytest
import asyncio
from typing import Annotated
from good_common.pipeline import Pipeline, Attribute, function_mapper


# Test data for the tests
@pytest.fixture
def basic_pipeline():
    def add(a: int, b: int) -> Annotated[int, Attribute("result")]:
        return a + b

    def multiply(result: int, factor: int) -> Annotated[int, Attribute("result")]:
        return result * factor

    return Pipeline(add, multiply)


@pytest.fixture
def async_pipeline():
    async def async_add(a: int, b: int) -> Annotated[int, Attribute("sum")]:
        await asyncio.sleep(0.1)
        return a + b

    async def async_multiply(
        sum: int, factor: int
    ) -> Annotated[int, Attribute("product")]:
        await asyncio.sleep(0.1)
        return sum * factor

    return Pipeline(async_add, async_multiply)


@pytest.fixture
def mixed_pipeline():
    async def async_add(a: int, b: int) -> Annotated[int, Attribute("sum")]:
        await asyncio.sleep(0.1)
        return a + b

    def sync_multiply(sum: int, factor: int) -> Annotated[int, Attribute("product")]:
        return sum * factor

    return Pipeline(async_add, sync_multiply)


# Test cases
@pytest.mark.asyncio
async def test_basic_sync_pipeline(basic_pipeline):
    output = await basic_pipeline(a=2, b=3, factor=4)
    assert output.result == 20


@pytest.mark.asyncio
async def test_async_pipeline(async_pipeline):
    output = await async_pipeline(a=2, b=3, factor=4)
    assert output.product == 20


@pytest.mark.asyncio
async def test_mixed_pipeline(mixed_pipeline):
    output = await mixed_pipeline(a=2, b=3, factor=4)
    assert output.product == 20


@pytest.mark.asyncio
async def test_pipeline_with_annotated_return_type():
    def create_greeting(name: str) -> Annotated[str, Attribute("greeting")]:
        return f"Hello, {name}!"

    # Wrap the print_greeting in a pipeline-compatible function
    def print_greeting(greeting: str) -> Annotated[None, Attribute("finished")]:
        print(f"Greeting: {greeting}")
        return None

    pipeline = Pipeline(create_greeting, print_greeting)
    output = await pipeline(name="Alice")
    assert output.greeting == "Hello, Alice!"


@pytest.mark.asyncio
async def test_pipeline_with_async_and_sync_mapped():
    async def async_subtract(x: int, y: int) -> Annotated[int, Attribute("diff")]:
        await asyncio.sleep(0.1)
        return x - y

    def multiply_diff(
        diff: int, factor: int
    ) -> Annotated[int, Attribute("final_result")]:
        return diff * factor

    # Fix the mapping and ensure 'diff' is correctly translated
    pipeline = Pipeline(async_subtract, function_mapper(multiply_diff, diff="diff"))

    output = await pipeline(x=10, y=3, factor=5)
    assert output.final_result == 35  # (10 - 3) * 5 = 35


@pytest.mark.asyncio
async def test_pipeline_parallel_execution():
    async def async_add(a: int, b: int) -> Annotated[int, Attribute("sum")]:
        await asyncio.sleep(0.1)
        return a + b

    def multiply(sum: int, factor: int) -> Annotated[int, Attribute("product")]:
        return sum * factor

    pipeline = Pipeline(async_add, multiply)

    inputs = [
        {"a": 1, "b": 2, "factor": 2},
        {"a": 2, "b": 3, "factor": 3},
        {"a": 3, "b": 4, "factor": 4},
    ]

    results = [
        result
        async for result in pipeline.execute(
            *inputs, max_workers=3, display_progress=False
        )
    ]

    assert results[0].unwrap().product == 6  # (1+2) * 2
    assert results[1].unwrap().product == 15  # (2+3) * 3
    assert results[2].unwrap().product == 28  # (3+4) * 4


@pytest.mark.asyncio
async def test_pipeline_with_errors():
    def faulty_add(a: int, b: int) -> Annotated[int, Attribute("result")]:
        raise ValueError("Deliberate error!")

    pipeline = Pipeline(faulty_add)

    with pytest.raises(ValueError, match="Deliberate error!"):
        await pipeline(a=1, b=2)


@pytest.mark.asyncio
async def test_pipeline_with_async_errors():
    async def async_faulty_add(a: int, b: int) -> Annotated[int, Attribute("result")]:
        await asyncio.sleep(0.1)
        raise ValueError("Deliberate async error!")

    pipeline = Pipeline(async_faulty_add)

    with pytest.raises(ValueError, match="Deliberate async error!"):
        await pipeline(a=1, b=2)


@pytest.mark.asyncio
async def test_pipeline_parallel_execution_with_errors():
    async def async_add(a: int, b: int) -> Annotated[int, Attribute("sum")]:
        await asyncio.sleep(0.1)
        if a == 2:
            raise ValueError("Error on purpose!")
        return a + b

    pipeline = Pipeline(async_add)

    inputs = [
        {"a": 1, "b": 2},
        {"a": 2, "b": 3},  # This one will raise an error
        {"a": 3, "b": 4},
    ]

    results = [
        result
        async for result in pipeline.execute(
            *inputs, max_workers=3, display_progress=False
        )
    ]

    assert results[0].is_ok() and results[0].unwrap().sum == 3
    assert results[1].is_err()
    assert results[2].is_ok() and results[2].unwrap().sum == 7
