from collections import defaultdict
from dataclasses import dataclass

# Import the functions and classes to be tested
from good_common.utilities._collections import (
    sort_object_keys,
    merge_dicts,
    deduplicate_dicts,
    clean_dict,
    recursive_remove_nones,
    set_defaults,
    merge_lists,
    flatten_list,
    recursive_to_dict,
    to_dict,
    map_object,
    expand_nested_json,
    recursive_default,
    recursive_get,
    recursive_convert_lists,
    index_object,
    deindex_object,
    DotDict,
    dict_to_flatdict,
    flatdict_to_dict,
    flatten_seq,
)


def test_sort_object_keys():
    obj = {"b": 2, "a": 1}
    result = sort_object_keys(obj)
    assert result == {"a": 1, "b": 2}


# Test merge_dicts
def test_merge_dicts():
    d1 = {"a": 1, "b": {"c": 2}}
    d2 = {"b": {"d": 3}, "e": 4}
    result = merge_dicts([d1, d2])
    assert result == {"a": 1, "b": {"c": 2, "d": 3}, "e": 4}

    # Test with keep_unique_values
    d1 = {"a": 1, "b": 2}
    d2 = {"a": 3, "c": 4}
    result = merge_dicts([d1, d2], keep_unique_values=True)
    assert result == {"a": [1, 3], "b": 2, "c": 4}


# Test deduplicate_dicts
def test_deduplicate_dicts():
    dicts = [{"a": 1}, {"b": 2}, {"a": 1}, {"c": 3}]
    result = deduplicate_dicts(dicts)
    assert result == [{"a": 1}, {"b": 2}, {"c": 3}]


# Test clean_dict
def test_clean_dict():
    d = defaultdict(list, {"a": [1, 2], "b": {"c": set([3, 4])}})
    result = clean_dict(d)
    assert isinstance(result, dict)
    assert result == {"a": [1, 2], "b": {"c": [3, 4]}}


# Test recursive_remove_nones
def test_recursive_remove_nones():
    d = {"a": 1, "b": None, "c": {"d": 2, "e": None}}
    result = recursive_remove_nones(d)
    assert result == {"a": 1, "c": {"d": 2}}


# Test set_defaults
def test_set_defaults():
    base = {"a": 1}
    result = set_defaults(base, b=2, c=3)
    assert result == {"a": 1, "b": 2, "c": 3}


# Test merge_lists
def test_merge_lists():
    lists = [[1, 2], [2, 3], [3, 4]]
    result = merge_lists(lists)
    assert result == [1, 2, 3, 4]


# Test flatten_list
def test_flatten_list():
    lst = [1, [2, 3, [4, 5]], 6]
    result = flatten_list(lst)
    assert result == [1, 2, 3, 4, 5, 6]


# Test recursive_to_dict
def test_recursive_to_dict():
    class TestObj:
        def __init__(self):
            self.a = 1
            self.b = {"c": 2}

    obj = TestObj()
    result = recursive_to_dict(obj)
    assert result == {"a": 1, "b": {"c": 2}}


# Test to_dict
def test_to_dict():
    @dataclass
    class TestDataclass:
        a: int
        b: dict

    obj = TestDataclass(a=1, b={"c": 2})
    result = to_dict(obj)
    assert result == {"a": 1, "b": {"c": 2}}


# Test map_object
def test_map_object():
    obj = {"a": "1", "b": "2", "c": "3"}
    result = map_object(obj, a=int, b=float)
    assert result == {"a": 1, "b": 2.0, "c": "3"}


# Test expand_nested_json
def test_expand_nested_json():
    obj = {"a": 1, "b": '{"c": 2, "d": {"e": 3}}'}
    result = expand_nested_json(obj)
    assert result == {"a": 1, "b": {"c": 2, "d": {"e": 3}}}


# Test recursive_default
def test_recursive_default():
    obj = {"a": {"b": 1}, "c": 2}
    assert recursive_default(obj, "a", "b") == 1
    assert recursive_default(obj, "c") == 2
    assert recursive_default(obj, "e", "f") is None


# Test recursive_get
def test_recursive_get():
    obj = {"a": {"b": {"c": 1}}}
    assert recursive_get(obj, "a", "b", "c") == 1
    assert recursive_get(obj, "a", "b", "d") is None


# Test recursive_convert_lists
def test_recursive_convert_lists():
    obj = {"a": {"0": "x", "1": "y"}, "b": {"0": "z"}}
    result = recursive_convert_lists(obj)
    assert result == {"a": ["x", "y"], "b": ["z"]}


# Test index_object and deindex_object
# def test_index_deindex_object():
#     obj = {"a": {"b": [1, 2, {"c": 3}]}}
#     indexed = index_object(obj)
#     assert indexed == {"a.b[0]": 1, "a.b[1]": 2, "a.b[2].c": 3}
#     deindexed = deindex_object(indexed)
#     assert deindexed == obj


def test_index_deindex_object():
    obj = {"a": {"b": [1, 2, {"c": 3}]}}
    indexed = index_object(obj)
    assert indexed == {"a.b[0]": 1, "a.b[1]": 2, "a.b[2].c": 3}
    deindexed = deindex_object(indexed)
    assert deindexed == obj

    # Additional test with more complex structure
    complex_obj = {"x": [{"y": 1}, 2, [3, {"z": 4}]]}
    complex_indexed = index_object(complex_obj)
    assert complex_indexed == {"x[0].y": 1, "x[1]": 2, "x[2][0]": 3, "x[2][1].z": 4}
    complex_deindexed = deindex_object(complex_indexed)
    assert complex_deindexed == complex_obj


# Test DotDict
def test_dotdict():
    d = DotDict({"a": 1, "b": {"c": 2}})
    assert d.a == 1
    assert d.b.c == 2
    d.d = {"e": 3}
    assert d.d.e == 3
    assert d["d"]["e"] == 3
    d.f = [{"g": 4}, {"h": 5}]
    assert d.f[0].g == 4
    assert d.f[1].h == 5

    # Test conversion back to dict
    regular_dict = d.to_dict()
    assert isinstance(regular_dict, dict)
    assert not isinstance(regular_dict["b"], DotDict)
    assert regular_dict == {
        "a": 1,
        "b": {"c": 2},
        "d": {"e": 3},
        "f": [{"g": 4}, {"h": 5}],
    }


# Test dict_to_flatdict and flatdict_to_dict
def test_dict_flatdict_conversion():
    nested = {"a": 1, "b": {"c": 2, "d": {"e": 3}}}
    flat = dict_to_flatdict(nested)
    assert flat == {("a",): 1, ("b", "c"): 2, ("b", "d", "e"): 3}
    restored = flatdict_to_dict(flat)
    assert restored == nested


# Test flatten_seq
def test_flatten_seq():
    seq = [1, [2, 3, [4, 5]], 6]
    result = list(flatten_seq(seq))
    assert result == [1, 2, 3, 4, 5, 6]
