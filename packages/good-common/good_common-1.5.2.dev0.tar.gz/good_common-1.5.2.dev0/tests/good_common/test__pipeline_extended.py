"""Extended tests for Pipeline to improve coverage from 63% to 85%+

Focus areas:
- Output class type checking and validation
- PipelineResult iterator protocols
- Pipeline registration errors and edge cases
- Synchronous execution modes
- Debug mode and defaults
- Error handling in different scenarios
"""

import pytest
import asyncio
from typing import Annotated
from good_common.pipeline import (
    Pipeline,
    Attribute,
    function_mapper,
    Output,
    AbstractComponent,
)
from good_common.pipeline._pipeline import PipelineResult
from result import Ok, Err


class TestOutputClass:
    """Test Output class type checking, locking, and edge cases"""

    def test_output_type_checking_simple(self):
        """Test type checking for simple types"""
        output = Output()
        output.register("value", "int")
        output.value = 42
        assert output.value == 42

    def test_output_type_checking_simple_invalid(self):
        """Test type checking fails for wrong simple types"""
        output = Output()
        output.register("value", "int")
        with pytest.raises(TypeError, match="must be of type"):
            output.value = "not an int"

    def test_output_without_type_checking(self):
        """Test output can accept values without registration"""
        output = Output()
        output.value = 42
        output.name = "test"
        assert output.value == 42
        assert output.name == "test"

    def test_output_locked(self):
        """Test that locked output prevents new attributes"""
        output = Output()
        output.register("value", "int")
        output.value = 42
        output.lock()
        with pytest.raises(AttributeError, match="Output is locked"):
            output.new_value = 100

    def test_output_locked_blocks_all_sets(self):
        """Test that locked output blocks all attribute sets"""
        output = Output()
        output.register("value", "int")
        output.value = 42
        output.lock()
        # Once locked, even registered attributes can't be set
        with pytest.raises(AttributeError, match="Output is locked"):
            output.value = 100

    def test_output_copy(self):
        """Test output copy creates independent instance"""
        output = Output()
        output.register("value", "int")
        output.value = 42
        copy = output.copy()
        copy.value = 100
        assert output.value == 42
        assert copy.value == 100

    def test_output_as_dict(self):
        """Test output as_dict returns data copy"""
        output = Output()
        output.register("a", "int")
        output.register("b", "str")
        output.a = 1
        output.b = "test"
        data = output.as_dict()
        assert data == {"a": 1, "b": "test"}
        # Modify dict shouldn't affect output
        data["c"] = 3
        assert not hasattr(output, "c")

    def test_output_repr(self):
        """Test output repr shows registered types"""
        output = Output()
        output.register("value", "int")
        output.register("name", "str")
        repr_str = repr(output)
        assert "value: int" in repr_str
        assert "name: str" in repr_str

    def test_output_getattr_missing(self):
        """Test getting non-existent attribute raises AttributeError"""
        output = Output()
        with pytest.raises(AttributeError, match="not found"):
            _ = output.missing_attr


class TestPipelineResult:
    """Test PipelineResult iterator protocols"""

    def test_pipeline_result_sync_iterator(self):
        """Test synchronous iteration over PipelineResult"""

        def gen():
            yield Ok(1)
            yield Ok(2)
            yield Err(ValueError("error"))

        result = PipelineResult(sync_generator=gen())
        items = list(result)
        assert len(items) == 3
        assert items[0].is_ok()
        assert items[1].is_ok()
        assert items[2].is_err()

    @pytest.mark.asyncio
    async def test_pipeline_result_async_iterator(self):
        """Test asynchronous iteration over PipelineResult"""

        async def gen():
            yield Ok(1)
            yield Ok(2)
            yield Err(ValueError("error"))

        result = PipelineResult(async_generator=gen())
        items = []
        async for item in result:
            items.append(item)
        assert len(items) == 3
        assert items[0].is_ok()
        assert items[1].is_ok()
        assert items[2].is_err()

    @pytest.mark.asyncio
    async def test_pipeline_result_async_from_sync(self):
        """Test async iteration wraps sync generator"""

        def gen():
            yield Ok(1)
            yield Ok(2)

        result = PipelineResult(sync_generator=gen())
        items = []
        async for item in result:
            items.append(item)
        assert len(items) == 2
        assert all(item.is_ok() for item in items)

    def test_pipeline_result_iter_on_async_fails(self):
        """Test that sync iteration fails on async-only result"""

        async def gen():
            yield Ok(1)

        result = PipelineResult(async_generator=gen())
        with pytest.raises(TypeError, match="Cannot use __iter__ on an async"):
            list(result)

    def test_pipeline_result_repr(self):
        """Test PipelineResult repr"""

        def gen():
            yield Ok(1)

        result = PipelineResult(sync_generator=gen())
        repr_str = repr(result)
        assert "PipelineResult" in repr_str


class TestPipelineEdgeCases:
    """Test Pipeline edge cases and error conditions"""

    def test_pipeline_apply_method(self):
        """Test pipeline apply method adds functions"""

        def add(a: int, b: int) -> Annotated[int, Attribute("result")]:
            return a + b

        def multiply(result: int, c: int) -> Annotated[int, Attribute("final")]:
            return result * c

        pipeline = Pipeline(add)
        pipeline.apply(multiply)
        output = pipeline.run_sync(a=2, b=3, c=4)
        assert output.final == 20

    def test_pipeline_slot_type_conflict(self):
        """Test that conflicting slot types raise error"""

        def step1(a: int) -> Annotated[str, Attribute("result")]:
            return str(a)

        def step2(result: int) -> Annotated[int, Attribute("output")]:
            return result * 2

        with pytest.raises(ValueError, match="already exists with type"):
            Pipeline(step1, step2)

    def test_pipeline_missing_input(self):
        """Test that missing required input raises error"""

        def add(a: int, b: int) -> Annotated[int, Attribute("result")]:
            return a + b

        pipeline = Pipeline(add)
        with pytest.raises(ValueError, match="Missing input"):
            pipeline.run_sync(a=1)  # Missing 'b'

    def test_pipeline_multiple_inputs_same_type(self):
        """Test pipeline with multiple inputs of same type"""

        def step1(a: int, b: int) -> Annotated[int, Attribute("sum")]:
            return a + b

        def step2(sum: int, c: int) -> Annotated[int, Attribute("result")]:
            return sum * c

        pipeline = Pipeline(step1, step2)
        output = pipeline.run_sync(a=2, b=3, c=4)
        assert output.result == 20

    def test_pipeline_anonymous_type_not_in_params(self):
        """Test that anonymous type not in params raises error"""

        def step1() -> int:
            return 42

        with pytest.raises(ValueError, match="not found in function"):
            Pipeline(step1)

    def test_pipeline_construction_with_defaults(self):
        """Test pipeline can be constructed with default parameters"""

        def add(a: int, b: int) -> Annotated[int, Attribute("result")]:
            return a + b

        def multiply(result: int, factor: int) -> Annotated[int, Attribute("final")]:
            return result * factor

        # Defaults are stored in pipeline._defaults
        pipeline = Pipeline(add, multiply, factor=10)
        assert pipeline._defaults == {"factor": 10}
        assert hasattr(pipeline._output, "factor")
        assert pipeline._output.factor == 10

    @pytest.mark.asyncio
    async def test_pipeline_defaults_preserved_in_output(self):
        """Test default values are accessible in pipeline output object"""

        def process(x: int, multiplier: int) -> Annotated[int, Attribute("result")]:
            return x * multiplier

        pipeline = Pipeline(process, multiplier=5)
        # Verify default is in the output object
        assert hasattr(pipeline._output, "multiplier")
        assert pipeline._output.multiplier == 5

    def test_pipeline_debug_mode(self):
        """Test pipeline debug mode logs execution"""

        def add(a: int, b: int) -> Annotated[int, Attribute("result")]:
            return a + b

        pipeline = Pipeline(add, debug=True)
        output = pipeline.run_sync(a=2, b=3)
        assert output.result == 5

    @pytest.mark.asyncio
    async def test_pipeline_debug_mode_async(self):
        """Test async pipeline debug mode"""

        async def add(a: int, b: int) -> Annotated[int, Attribute("result")]:
            return a + b

        pipeline = Pipeline(add, debug=True)
        output = await pipeline(a=2, b=3)
        assert output.result == 5

    def test_pipeline_copy(self):
        """Test pipeline copy creates independent instance"""

        def add(a: int, b: int) -> Annotated[int, Attribute("result")]:
            return a + b

        pipeline = Pipeline(add)
        copy = pipeline.copy()
        assert copy._steps == pipeline._steps
        assert copy._pipeline == pipeline._pipeline
        assert copy._slots == pipeline._slots

    def test_pipeline_repr(self):
        """Test pipeline repr shows slots"""

        def add(a: int, b: int) -> Annotated[int, Attribute("result")]:
            return a + b

        pipeline = Pipeline(add)
        repr_str = repr(pipeline)
        assert "Pipeline" in repr_str
        assert "a:" in repr_str
        assert "b:" in repr_str


class TestSyncExecution:
    """Test synchronous execution modes"""

    def test_sync_execute_preserve_order(self):
        """Test sync execution preserves order"""

        def add(a: int, b: int) -> Annotated[int, Attribute("result")]:
            return a + b

        pipeline = Pipeline(add)
        inputs = [{"a": 1, "b": 2}, {"a": 3, "b": 4}, {"a": 5, "b": 6}]
        results = list(
            pipeline.sync_execute(*inputs, max_workers=2, display_progress=False)
        )
        assert len(results) == 3
        assert results[0].unwrap().result == 3
        assert results[1].unwrap().result == 7
        assert results[2].unwrap().result == 11

    def test_sync_execute_no_preserve_order(self):
        """Test sync execution without order preservation"""

        def add(a: int, b: int) -> Annotated[int, Attribute("result")]:
            return a + b

        pipeline = Pipeline(add)
        inputs = [{"a": 1, "b": 2}, {"a": 3, "b": 4}, {"a": 5, "b": 6}]
        results = list(
            pipeline.sync_execute(
                *inputs, max_workers=2, preserve_order=False, display_progress=False
            )
        )
        assert len(results) == 3
        # Results may be in any order
        result_values = sorted([r.unwrap().result for r in results])
        assert result_values == [3, 7, 11]

    def test_sync_execute_with_error(self):
        """Test sync execution handles errors"""

        def add(a: int, b: int) -> Annotated[int, Attribute("result")]:
            if a == 3:
                raise ValueError("Error at a=3")
            return a + b

        pipeline = Pipeline(add)
        inputs = [{"a": 1, "b": 2}, {"a": 3, "b": 4}, {"a": 5, "b": 6}]
        results = list(
            pipeline.sync_execute(*inputs, max_workers=2, display_progress=False)
        )
        assert len(results) == 3
        assert results[0].is_ok()
        assert results[1].is_err()
        assert results[2].is_ok()

    def test_execute_detects_sync_pipeline(self):
        """Test execute() method detects sync pipeline"""

        def add(a: int, b: int) -> Annotated[int, Attribute("result")]:
            return a + b

        pipeline = Pipeline(add)
        inputs = [{"a": 1, "b": 2}, {"a": 3, "b": 4}]
        result = pipeline.execute(*inputs, max_workers=2, display_progress=False)
        assert isinstance(result, PipelineResult)
        results = list(result)
        assert len(results) == 2
        assert all(r.is_ok() for r in results)

    @pytest.mark.asyncio
    async def test_execute_detects_async_pipeline(self):
        """Test execute() method detects async pipeline"""

        async def add(a: int, b: int) -> Annotated[int, Attribute("result")]:
            await asyncio.sleep(0.01)
            return a + b

        pipeline = Pipeline(add)
        inputs = [{"a": 1, "b": 2}, {"a": 3, "b": 4}]
        result = pipeline.execute(*inputs, max_workers=2, display_progress=False)
        assert isinstance(result, PipelineResult)
        results = []
        async for r in result:
            results.append(r)
        assert len(results) == 2
        assert all(r.is_ok() for r in results)

    def test_sync_execute_with_progress(self):
        """Test sync execution with progress display"""

        def add(a: int, b: int) -> Annotated[int, Attribute("result")]:
            return a + b

        pipeline = Pipeline(add)
        inputs = [{"a": 1, "b": 2}, {"a": 3, "b": 4}]
        # Just verify it doesn't crash with progress enabled
        results = list(
            pipeline.sync_execute(*inputs, max_workers=2, display_progress=True)
        )
        assert len(results) == 2


class TestAbstractComponent:
    """Test AbstractComponent base class"""

    def test_abstract_component_name(self):
        """Test AbstractComponent __name__ property"""

        class MyComponent(AbstractComponent):
            def __call__(self, x: int) -> Annotated[int, Attribute("result")]:
                return x * 2

        component = MyComponent()
        assert component.__name__ == "MyComponent"

    @pytest.mark.asyncio
    async def test_abstract_component_in_pipeline(self):
        """Test using AbstractComponent in pipeline"""

        class Doubler(AbstractComponent):
            def __call__(self, x: int) -> Annotated[int, Attribute("doubled")]:
                return x * 2

        class Adder(AbstractComponent):
            def __call__(self, doubled: int, y: int) -> Annotated[int, Attribute("result")]:
                return doubled + y

        pipeline = Pipeline(Doubler(), Adder())
        output = await pipeline(x=5, y=3)
        assert output.result == 13


class TestFunctionMapper:
    """Test function_mapper utility"""

    def test_function_mapper_basic(self):
        """Test function mapper renames parameters"""

        def process(value: int, factor: int) -> int:
            return value * factor

        # Map 'x' to 'value', 'y' to 'factor'
        mapped = function_mapper(process, x="value", y="factor")
        result = mapped(x=10, y=2)
        assert result == 20

    def test_function_mapper_preserves_unmapped(self):
        """Test function mapper preserves unmapped parameters"""

        def process(a: int, b: int, c: int) -> int:
            return a + b + c

        # Only map 'x' to 'a'
        mapped = function_mapper(process, x="a")
        result = mapped(x=1, b=2, c=3)
        assert result == 6


class TestMultipleReturnValues:
    """Test pipeline with multiple return values"""

    @pytest.mark.asyncio
    async def test_multiple_return_annotated(self):
        """Test function with multiple annotated return values"""

        def compute(
            x: int, y: int
        ) -> tuple[Annotated[int, Attribute("sum")], Annotated[int, Attribute("product")]]:
            return (x + y, x * y)

        def final(
            sum: int, product: int
        ) -> Annotated[int, Attribute("result")]:
            return sum + product

        pipeline = Pipeline(compute, final)
        output = await pipeline(x=3, y=4)
        assert output.sum == 7
        assert output.product == 12
        assert output.result == 19

    def test_multiple_return_sync(self):
        """Test sync pipeline with multiple return values"""

        def compute(
            x: int, y: int
        ) -> tuple[Annotated[int, Attribute("sum")], Annotated[int, Attribute("diff")]]:
            return (x + y, x - y)

        pipeline = Pipeline(compute)
        output = pipeline.run_sync(x=10, y=3)
        assert output.sum == 13
        assert output.diff == 7


class TestRunSyncWithAsyncFunctions:
    """Test run_sync handling of async functions"""

    def test_run_sync_with_async_function(self):
        """Test that run_sync can handle async functions"""

        async def async_add(a: int, b: int) -> Annotated[int, Attribute("result")]:
            await asyncio.sleep(0.01)
            return a + b

        pipeline = Pipeline(async_add)
        output = pipeline.run_sync(a=5, b=3)
        assert output.result == 8

    def test_run_sync_with_mixed_functions(self):
        """Test run_sync with both sync and async functions"""

        def sync_double(x: int) -> Annotated[int, Attribute("doubled")]:
            return x * 2

        async def async_add(doubled: int, y: int) -> Annotated[int, Attribute("result")]:
            await asyncio.sleep(0.01)
            return doubled + y

        pipeline = Pipeline(sync_double, async_add)
        output = pipeline.run_sync(x=5, y=3)
        assert output.result == 13
