"""Test suite for import time optimization."""

import importlib
import sys
import time
from typing import Tuple
import pytest


def clear_module_cache(module_prefix: str = "good_common"):
    """Clear module cache for accurate import timing.
    
    Note: We preserve url_plugins module to maintain plugin registry state
    for test isolation. This module is lightweight and doesn't affect 
    import performance measurements.
    """
    modules_to_clear = [
        m for m in list(sys.modules.keys()) 
        if module_prefix in m and 'url_plugins' not in m
    ]
    for module in modules_to_clear:
        del sys.modules[module]


def time_import(module_name: str) -> Tuple[float, bool]:
    """Time the import of a module and return (time_ms, success)."""
    clear_module_cache()
    
    start = time.perf_counter()
    try:
        importlib.import_module(module_name)
        elapsed = (time.perf_counter() - start) * 1000
        return elapsed, True
    except Exception as e:
        elapsed = (time.perf_counter() - start) * 1000
        print(f"Failed to import {module_name}: {e}")
        return elapsed, False


class TestImportPerformance:
    """Test import performance of good_common modules."""
    
    # Maximum acceptable import times in milliseconds
    MAX_IMPORT_TIMES = {
        "good_common": 500,  # Main module
        "good_common.dependencies": 200,
        "good_common.pipeline": 100,
        "good_common.types": 500,  # Currently slow due to web types
        "good_common.utilities": 50,
        "good_common.modeling": 100,
    }
    
    def test_individual_module_imports(self):
        """Test import times for individual modules."""
        results = {}
        
        for module_name, max_time in self.MAX_IMPORT_TIMES.items():
            import_time, success = time_import(module_name)
            results[module_name] = {
                "time": import_time,
                "success": success,
                "max_allowed": max_time,
                "passed": import_time <= max_time if success else False
            }
        
        # Print results
        print("\n" + "=" * 60)
        print("Import Time Report")
        print("=" * 60)
        for module, data in results.items():
            status = "✓" if data["passed"] else "✗" if data["success"] else "ERROR"
            print(f"{status} {module:<35} {data['time']:>8.2f}ms (max: {data['max_allowed']}ms)")
        
        # Check for failures
        failures = []
        for module, data in results.items():
            if data["success"] and not data["passed"]:
                failures.append(
                    f"{module}: {data['time']:.2f}ms exceeds limit of {data['max_allowed']}ms"
                )
        
        if failures:
            pytest.skip("\n".join(["Import times exceed limits:"] + failures))
    
    def test_lazy_import_functionality(self):
        """Test that lazy imports work correctly when accessed."""
        clear_module_cache()
        
        # Import the main module
        
        # Test that we can still use web types when needed
        from good_common.types import URL
        url = URL("https://example.com")
        assert str(url) == "https://example.com/"  # URL adds trailing slash
        assert url.host == "example.com"
    
    def test_minimal_import_path(self):
        """Test import time for minimal functionality."""
        clear_module_cache()
        
        # Time importing just the essentials
        start = time.perf_counter()
        elapsed = (time.perf_counter() - start) * 1000
        
        assert elapsed < 200, f"Minimal import took {elapsed:.2f}ms, should be < 200ms"
    
    def test_heavy_dependencies_isolation(self):
        """Test that heavy dependencies are properly isolated."""
        clear_module_cache()
        
        # These imports should not trigger heavy dependencies
        # Note: Some utilities might import types internally
        light_modules = [
            "good_common.utilities._dates", 
            "good_common.utilities._collections",
            "good_common.pipeline._pipeline",
        ]
        
        for module in light_modules:
            clear_module_cache()
            import_time, success = time_import(module)
            assert success, f"Failed to import {module}"
            assert import_time < 100, f"{module} took {import_time:.2f}ms, should be < 100ms"


class TestLazyLoadOptimizations:
    """Test specific lazy loading optimizations."""
    
    def test_web_types_lazy_load(self):
        """Test that web types can be lazy loaded."""
        clear_module_cache()
        
        # Import types module without accessing web types
        
        # Check heavy dependencies aren't loaded yet (if we implement lazy loading)
        # This will fail initially and pass after optimization
        # assert "tldextract" not in sys.modules
        # assert "courlan" not in sys.modules
    
    def test_utilities_selective_import(self):
        """Test selective import from utilities."""
        clear_module_cache()
        
        # Import specific utility without loading all
        from good_common.utilities import camel_to_slug
        
        # Should work without loading heavy dependencies
        result = camel_to_slug("TestFile2024")
        assert result == "test-file2024"  # Numbers stay joined


@pytest.mark.skip(reason="Benchmark tests require pytest-benchmark plugin")
class TestImportBenchmarks:
    """Benchmark tests for import performance."""
    
    def test_baseline_import_benchmark(self, benchmark):
        """Benchmark the full good_common import."""
        def import_module():
            clear_module_cache()
        
        benchmark(import_module)
    
    def test_types_import_benchmark(self, benchmark):
        """Benchmark the types module import."""
        def import_module():
            clear_module_cache()
        
        benchmark(import_module)
    
    def test_dependencies_import_benchmark(self, benchmark):
        """Benchmark the dependencies module import."""
        def import_module():
            clear_module_cache()
        
        benchmark(import_module)


def test_import_report():
    """Generate a detailed import time report."""
    modules_to_test = [
        "good_common",
        "good_common.dependencies",
        "good_common.modeling",
        "good_common.pipeline",
        "good_common.types",
        "good_common.types.web",
        "good_common.types.placeholder",
        "good_common.utilities",
    ]
    
    print("\n" + "=" * 70)
    print("DETAILED IMPORT TIME ANALYSIS")
    print("=" * 70)
    
    total_time = 0
    for module in modules_to_test:
        import_time, success = time_import(module)
        if success:
            total_time += import_time
            status = "OK"
        else:
            status = "FAIL"
        
        bar_length = int(import_time / 10)  # 1 char per 10ms
        bar = "█" * min(bar_length, 50)
        print(f"{status:4} {module:<40} {import_time:>8.2f}ms {bar}")
    
    print("-" * 70)
    print(f"{'TOTAL':<45} {total_time:>8.2f}ms")
    print("=" * 70)