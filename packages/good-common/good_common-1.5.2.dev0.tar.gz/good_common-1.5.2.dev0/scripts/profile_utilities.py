#!/usr/bin/env python
"""Profile utility functions to identify performance bottlenecks."""

import random
import string
import cProfile
import pstats
import io

# Setup path
import sys
sys.path.insert(0, 'src')

from good_common.utilities._collections import (
    sort_object_keys,
    merge_dicts,
    deduplicate_dicts,
    flatten_list,
    recursive_get,
    index_object,
    deindex_object,
)
from good_common.utilities._strings import (
    camel_to_snake,
    detect_string_type,
)
from good_common.utilities._functional import (
    filter_nulls,
    deep_attribute_get
)

def generate_test_data():
    """Generate test data for profiling."""
    
    # Large nested dictionary
    large_dict = {}
    for i in range(100):
        large_dict[f"key_{i}"] = {
            "nested": {
                "value": random.randint(1, 1000),
                "list": [random.randint(1, 100) for _ in range(10)],
                "string": ''.join(random.choices(string.ascii_letters, k=50))
            }
        }
    
    # List of dictionaries for deduplication
    dict_list = []
    for _ in range(500):
        dict_list.append({
            "id": random.randint(1, 50),  # Intentional duplicates
            "value": random.random(),
            "name": ''.join(random.choices(string.ascii_letters, k=10))
        })
    
    # Nested list for flattening
    nested_list = [[[[i] * 5] for i in range(10)] for _ in range(20)]
    
    # String list for type detection
    strings = [
        "https://example.com/image.jpg",
        "test@email.com", 
        "2024-01-01",
        '{"key": "value"}',
        "some random text",
        "550e8400-e29b-41d4-a716-446655440000"
    ] * 100
    
    return large_dict, dict_list, nested_list, strings

def profile_sort_operations(data):
    """Profile sorting operations."""
    for _ in range(100):
        sort_object_keys(data)

def profile_merge_operations(dict_list):
    """Profile merge operations."""
    chunks = [dict_list[i:i+10] for i in range(0, len(dict_list), 10)]
    for chunk in chunks:
        merge_dicts(chunk)

def profile_deduplication(dict_list):
    """Profile deduplication."""
    for _ in range(10):
        deduplicate_dicts(dict_list)

def profile_flatten(nested_list):
    """Profile list flattening."""
    for _ in range(100):
        flatten_list(nested_list)

def profile_recursive_get(data):
    """Profile recursive get operations."""
    for _ in range(1000):
        recursive_get(data, "key_50", "nested", "value")
        recursive_get(data, "key_99", "nested", "list")

def profile_index_deindex(data):
    """Profile index/deindex operations."""
    for _ in range(50):
        indexed = index_object(data)
        deindex_object(indexed)

def profile_string_operations(strings):
    """Profile string operations."""
    for s in strings:
        detect_string_type(s)
        if len(s) > 10:
            camel_to_snake(s[:20])

def profile_filter_nulls(data):
    """Profile null filtering."""
    # Add some nulls
    data_with_nulls = data.copy()
    for i in range(0, 100, 3):
        data_with_nulls[f"key_{i}"]["nested"]["null_field"] = None
        data_with_nulls[f"key_{i}"]["empty_list"] = []
        
    for _ in range(100):
        filter_nulls(data_with_nulls)

def profile_deep_attribute_get(data):
    """Profile deep attribute get."""
    for _ in range(500):
        deep_attribute_get(data, "key_*.nested.value")
        deep_attribute_get(data, "key_42.nested.list[*]")

def main():
    print("Generating test data...")
    large_dict, dict_list, nested_list, strings = generate_test_data()
    
    print("\nProfiling utility functions...")
    
    # Create profiler
    pr = cProfile.Profile()
    
    # Start profiling
    pr.enable()
    
    # Run operations
    print("- Sorting operations")
    profile_sort_operations(large_dict)
    
    print("- Merge operations") 
    profile_merge_operations(dict_list)
    
    print("- Deduplication")
    profile_deduplication(dict_list)
    
    print("- Flattening")
    profile_flatten(nested_list)
    
    print("- Recursive get")
    profile_recursive_get(large_dict)
    
    print("- Index/deindex")
    profile_index_deindex(large_dict)
    
    print("- String operations")
    profile_string_operations(strings)
    
    print("- Filter nulls")
    profile_filter_nulls(large_dict)
    
    print("- Deep attribute get")
    profile_deep_attribute_get(large_dict)
    
    # Stop profiling
    pr.disable()
    
    # Print statistics
    print("\n" + "="*60)
    print("PERFORMANCE PROFILE RESULTS")
    print("="*60)
    
    s = io.StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
    ps.print_stats(30)  # Top 30 functions
    print(s.getvalue())
    
    # Also print by time
    print("\n" + "="*60)
    print("TOP TIME CONSUMERS")
    print("="*60)
    s = io.StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats('time')
    ps.print_stats(20)
    print(s.getvalue())

if __name__ == "__main__":
    main()