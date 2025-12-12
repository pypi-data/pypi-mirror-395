#!/usr/bin/env python
"""
Benchmark script comparing pure Python vs Cython optimized functions.
"""

import time
import random
import string
import sys
from typing import Callable
import statistics

# Add src to path
sys.path.insert(0, 'src')

# Import pure Python versions
from good_common.utilities._collections import (
    sort_object_keys as sort_object_keys_py,
    index_object as index_object_py,
    deindex_object as deindex_object_py,
    merge_dicts as merge_dicts_py,
    deduplicate_dicts as deduplicate_dicts_py,
    flatten_list as flatten_list_py,
    recursive_get as recursive_get_py,
)

from good_common.utilities._functional import (
    filter_nulls as filter_nulls_py,
    deep_attribute_get as deep_attribute_get_py,
)

from good_common.utilities._strings import (
    camel_to_snake as camel_to_snake_py,
    detect_string_type as detect_string_type_py,
    encode_base32 as encode_base32_py,
)

# Try to import Cython versions
try:
    from good_common.utilities._collections_cy import (
        sort_object_keys as sort_object_keys_cy,
        index_object as index_object_cy,
        deindex_object as deindex_object_cy,
        merge_dicts as merge_dicts_cy,
        deduplicate_dicts_cy,
        flatten_list as flatten_list_cy,
        recursive_get as recursive_get_cy,
    )
    CYTHON_COLLECTIONS = True
except ImportError:
    print("Warning: Cython collections module not available")
    CYTHON_COLLECTIONS = False
    # Fallback to Python versions
    sort_object_keys_cy = sort_object_keys_py
    index_object_cy = index_object_py
    deindex_object_cy = deindex_object_py
    merge_dicts_cy = merge_dicts_py
    deduplicate_dicts_cy = deduplicate_dicts_py
    flatten_list_cy = flatten_list_py
    recursive_get_cy = recursive_get_py

try:
    from good_common.utilities._functional_cy import (
        filter_nulls as filter_nulls_cy,
        deep_attribute_get as deep_attribute_get_cy,
    )
    CYTHON_FUNCTIONAL = True
except ImportError:
    print("Warning: Cython functional module not available")
    CYTHON_FUNCTIONAL = False
    filter_nulls_cy = filter_nulls_py
    deep_attribute_get_cy = deep_attribute_get_py

try:
    from good_common.utilities._strings_cy import (
        camel_to_snake as camel_to_snake_cy,
        detect_string_type as detect_string_type_cy,
        encode_base32 as encode_base32_cy,
    )
    CYTHON_STRINGS = True
except ImportError:
    print("Warning: Cython strings module not available")
    CYTHON_STRINGS = False
    camel_to_snake_cy = camel_to_snake_py
    detect_string_type_cy = detect_string_type_py
    encode_base32_cy = encode_base32_py


class Benchmark:
    """Benchmark runner for comparing function performance."""
    
    def __init__(self, name: str, iterations: int = 1000):
        self.name = name
        self.iterations = iterations
        self.results = {}
    
    def run(self, func: Callable, *args, **kwargs) -> float:
        """Run a function multiple times and return average time."""
        times = []
        for _ in range(self.iterations):
            start = time.perf_counter()
            func(*args, **kwargs)
            elapsed = time.perf_counter() - start
            times.append(elapsed)
        
        return statistics.mean(times)
    
    def compare(self, py_func: Callable, cy_func: Callable, *args, **kwargs):
        """Compare Python and Cython implementations."""
        print(f"\n{self.name}")
        print("-" * 50)
        
        # Run Python version
        py_time = self.run(py_func, *args, **kwargs)
        print(f"Python:  {py_time*1000:.4f} ms")
        
        # Run Cython version
        cy_time = self.run(cy_func, *args, **kwargs)
        print(f"Cython:  {cy_time*1000:.4f} ms")
        
        # Calculate speedup
        if cy_time > 0:
            speedup = py_time / cy_time
            print(f"Speedup: {speedup:.2f}x")
        else:
            print("Speedup: N/A (too fast to measure)")
        
        self.results[self.name] = {
            'python': py_time,
            'cython': cy_time,
            'speedup': py_time / cy_time if cy_time > 0 else float('inf')
        }
        
        return speedup


def generate_test_data():
    """Generate test data for benchmarks."""
    
    # Large nested dictionary
    large_dict = {}
    for i in range(100):
        large_dict[f"key_{i}"] = {
            "nested": {
                "value": random.randint(1, 1000),
                "list": [random.randint(1, 100) for _ in range(10)],
                "string": ''.join(random.choices(string.ascii_letters, k=50)),
                "null_field": None if i % 3 == 0 else i
            }
        }
    
    # List of dictionaries
    dict_list = []
    for _ in range(100):
        dict_list.append({
            "id": random.randint(1, 20),  # Intentional duplicates
            "value": random.random(),
            "name": ''.join(random.choices(string.ascii_letters, k=10))
        })
    
    # Nested list
    nested_list = [[[[i] * 3] for i in range(5)] for _ in range(10)]
    
    # String list
    strings = [
        "CamelCaseString",
        "HTMLParser",
        "XMLHttpRequest",
        "IOError",
        "https://example.com/path",
        "test@email.com",
        "2024-01-01",
        '{"key": "value"}',
    ] * 10
    
    return large_dict, dict_list, nested_list, strings


def main():
    print("="*60)
    print("CYTHON OPTIMIZATION BENCHMARK")
    print("="*60)
    
    print("\nCython Module Status:")
    print(f"  Collections: {'✓' if CYTHON_COLLECTIONS else '✗'}")
    print(f"  Functional:  {'✓' if CYTHON_FUNCTIONAL else '✗'}")
    print(f"  Strings:     {'✓' if CYTHON_STRINGS else '✗'}")
    
    if not any([CYTHON_COLLECTIONS, CYTHON_FUNCTIONAL, CYTHON_STRINGS]):
        print("\nNo Cython modules available. Building Cython extensions...")
        print("Run: python setup.py build_ext --inplace")
        return
    
    # Generate test data
    print("\nGenerating test data...")
    large_dict, dict_list, nested_list, strings = generate_test_data()
    
    # Collections benchmarks
    print("\n" + "="*60)
    print("COLLECTION OPERATIONS")
    print("="*60)
    
    bench = Benchmark("sort_object_keys (100 nested dicts)", 100)
    bench.compare(sort_object_keys_py, sort_object_keys_cy, large_dict)
    
    bench = Benchmark("index_object (100 nested dicts)", 100)
    bench.compare(index_object_py, index_object_cy, large_dict)
    
    indexed = index_object_py(large_dict)
    bench = Benchmark("deindex_object (indexed dict)", 100)
    bench.compare(deindex_object_py, deindex_object_cy, indexed)
    
    bench = Benchmark("merge_dicts (10 dicts)", 500)
    bench.compare(merge_dicts_py, merge_dicts_cy, dict_list[:10])
    
    bench = Benchmark("deduplicate_dicts (100 dicts)", 500)
    bench.compare(deduplicate_dicts_py, deduplicate_dicts_cy, dict_list)
    
    bench = Benchmark("flatten_list (nested list)", 1000)
    bench.compare(flatten_list_py, flatten_list_cy, nested_list)
    
    bench = Benchmark("recursive_get (nested access)", 10000)
    bench.compare(
        recursive_get_py, recursive_get_cy,
        large_dict, "key_50", "nested", "value"
    )
    
    # Functional benchmarks
    print("\n" + "="*60)
    print("FUNCTIONAL OPERATIONS")
    print("="*60)
    
    bench = Benchmark("filter_nulls (100 nested dicts)", 100)
    bench.compare(filter_nulls_py, filter_nulls_cy, large_dict)
    
    bench = Benchmark("deep_attribute_get (path access)", 1000)
    bench.compare(
        deep_attribute_get_py, deep_attribute_get_cy,
        large_dict, "key_42.nested.value"
    )
    
    # String benchmarks
    print("\n" + "="*60)
    print("STRING OPERATIONS")
    print("="*60)
    
    bench = Benchmark("camel_to_snake (80 strings)", 1000)
    for s in strings:
        if any(c.isupper() for c in s):
            camel_to_snake_py(s)
    py_time = bench.run(lambda: [camel_to_snake_py(s) for s in strings if any(c.isupper() for c in s)])
    cy_time = bench.run(lambda: [camel_to_snake_cy(s) for s in strings if any(c.isupper() for c in s)])
    print(f"Python:  {py_time*1000:.4f} ms")
    print(f"Cython:  {cy_time*1000:.4f} ms")
    print(f"Speedup: {py_time/cy_time:.2f}x")
    
    bench = Benchmark("detect_string_type (80 strings)", 1000)
    bench.compare(
        lambda: [detect_string_type_py(s) for s in strings],
        lambda: [detect_string_type_cy(s) for s in strings]
    )
    
    bench = Benchmark("encode_base32 (1000 integers)", 1000)
    numbers = [random.randint(0, 2**63) for _ in range(1000)]
    bench.compare(
        lambda: [encode_base32_py(n) for n in numbers],
        lambda: [encode_base32_cy(n) for n in numbers]
    )
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    
    total_speedup = []
    for name, result in bench.results.items():
        if result['speedup'] != float('inf'):
            total_speedup.append(result['speedup'])
    
    if total_speedup:
        avg_speedup = statistics.mean(total_speedup)
        median_speedup = statistics.median(total_speedup)
        print(f"\nAverage speedup: {avg_speedup:.2f}x")
        print(f"Median speedup:  {median_speedup:.2f}x")
        print(f"Best speedup:    {max(total_speedup):.2f}x")
        print(f"Worst speedup:   {min(total_speedup):.2f}x")
    
    print("\n✓ Benchmark complete!")


if __name__ == "__main__":
    main()