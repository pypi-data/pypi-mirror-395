import pytest
from nestedutils import get_path, set_path, del_path
from nestedutils.exceptions import PathError, PathErrorCode


# --------------------------------------------------------------
# BASIC GET
# --------------------------------------------------------------

def test_get_simple():
    d = {"a": 1}
    assert get_path(d, "a") == 1


def test_get_nested_dict():
    d = {"a": {"b": {"c": 5}}}
    assert get_path(d, "a.b.c") == 5


def test_get_missing_returns_default():
    d = {"a": {"b": 1}}
    assert get_path(d, "a.c", default=99) == 99
    assert get_path(d, "x.y.z") is None


def test_get_list_index():
    d = {"a": [10, 20, 30]}
    assert get_path(d, "a.1") == 20


def test_get_negative_list_index():
    d = {"a": [10, 20, 30]}
    assert get_path(d, "a.-1") == 30
    assert get_path(d, "a.-2") == 20


def test_get_nested_list_dict_mix():
    d = {"a": [{"b": 1}, {"b": 2}]}
    assert get_path(d, "a.1.b") == 2


# --------------------------------------------------------------
# BASIC SET
# --------------------------------------------------------------

def test_set_simple():
    d = {}
    set_path(d, "a", 5)
    assert d == {"a": 5}


def test_set_nested_existing():
    d = {"a": {"b": {}}}
    set_path(d, "a.b.c", 9)
    assert d == {"a": {"b": {"c": 9}}}


def test_set_auto_create_dicts():
    d = {}
    set_path(d, "x.y.z", 10)
    assert d == {"x": {"y": {"z": 10}}}


def test_set_auto_create_lists():
    d = {}
    set_path(d, "a.0.b", 1)
    assert d == {"a": [{"b": 1}]}


def test_set_auto_sparse_list():
    d = {"a": []}
    set_path(d, "a.5", 99)
    assert d == {"a": [None, None, None, None, None, 99]}


def test_set_negative_index_write():
    d = {"a": [1, 2, 3]}
    set_path(d, "a.-1", 999)
    assert d["a"] == [1, 2, 999]


def test_set_negative_index_extends_list():
    """Negative index on short list should still work"""
    d = {"a": [1]}
    set_path(d, "a.-1", 99)
    assert d == {"a": [99]}


def test_set_inside_list_of_dicts():
    d = {"a": [{}]}
    set_path(d, "a.0.x.y", 5)
    assert d == {"a": [{"x": {"y": 5}}]}


# --------------------------------------------------------------
# SET + FILL STRATEGY
# --------------------------------------------------------------

def test_set_fill_strategy_none():
    d = {}
    set_path(d, "a.3", 7, fill_strategy="none")
    assert d == {"a": [None, None, None, 7]}


def test_set_fill_strategy_dict():
    d = {}
    set_path(d, "a.0.b", 1, fill_strategy="dict")
    assert d == {"a": {"0": {"b": 1}}}


def test_set_fill_strategy_list():
    d = {}
    set_path(d, "a.0.1", 42, fill_strategy="list")
    assert d == {"a": [[None, 42]]}


def test_set_invalid_fill_strategy():
    d = {}
    with pytest.raises(PathError):
        set_path(d, "a.b", 1, fill_strategy="unknown")


def test_all_numeric_path_with_dict_strategy():
    """Numeric strings should be dict keys with dict strategy"""
    d = {}
    set_path(d, "0.1.2", 5, fill_strategy="dict")
    assert d == {"0": {"1": {"2": 5}}}


def test_all_numeric_path_with_auto_strategy():
    """All numeric path with auto should create nested lists"""
    d = {}
    set_path(d, "0.1", 5, fill_strategy="auto")
    # Creates nested lists when all keys are numeric


def test_multiple_operations_different_strategies():
    """Multiple sets with different strategies on same structure"""
    d = {}
    set_path(d, "a.0", 1, fill_strategy="auto")
    set_path(d, "a.5", 2, fill_strategy="dict")  # Should still be list
    assert isinstance(d["a"], list)
    assert len(d["a"]) == 6


# --------------------------------------------------------------
# SET WITH NONE VALUES
# --------------------------------------------------------------

def test_set_through_existing_none_in_list():
    """Should replace None with a container when navigating deeper"""
    d = {"a": [None, None, None]}
    set_path(d, "a.1.x", 5)
    assert d == {"a": [None, {"x": 5}, None]}


def test_set_through_none_created_by_sparse_fill():
    """Auto-filled None should be replaceable"""
    d = {}
    set_path(d, "a.5", 1)  # Creates [None, None, None, None, None, 1]
    set_path(d, "a.2.b", 99)  # Should replace None at index 2
    assert d["a"][2] == {"b": 99}


def test_set_through_none_in_dict():
    """Should replace None value in dict when navigating deeper"""
    d = {"a": None}
    set_path(d, "a.b.c", 10)
    assert d == {"a": {"b": {"c": 10}}}


def test_set_none_value_explicitly():
    """Setting None as a value should work"""
    d = {"a": 1}
    set_path(d, "a", None)
    assert d == {"a": None}


def test_set_none_in_nested_path():
    """Setting None deep in path"""
    d = {}
    set_path(d, "a.b.c", None)
    assert d == {"a": {"b": {"c": None}}}


# --------------------------------------------------------------
# SET INTO TUPLE (READ-ONLY)
# --------------------------------------------------------------

def test_set_into_tuple_fails():
    d = {"a": (1, 2, 3)}
    with pytest.raises(PathError):
        set_path(d, "a.0", 9)


def test_set_navigating_into_tuple_fails():
    d = {"a": ({"x": 1},)}
    with pytest.raises(PathError):
        set_path(d, "a.0.x.y", 1)


# --------------------------------------------------------------
# DELETE
# --------------------------------------------------------------

def test_delete_from_dict():
    d = {"a": {"b": 1}}
    val = del_path(d, "a.b")
    assert val == 1
    assert d == {"a": {}}


def test_delete_missing_key():
    d = {"a": {}}
    with pytest.raises(PathError):
        del_path(d, "a.b")


def test_delete_list_index_disallowed():
    d = {"a": [1, 2, 3]}
    with pytest.raises(PathError):
        del_path(d, "a.1")  # must explicitly allow list deletion


def test_delete_list_index_allowed():
    d = {"a": [1, 2, 3]}
    val = del_path(d, "a.1", allow_list_mutation=True)
    assert val == 2
    assert d == {"a": [1, 3]}


def test_delete_negative_index():
    d = {"a": [10, 20, 30]}
    val = del_path(d, "a.-1", allow_list_mutation=True)
    assert val == 30
    assert d == {"a": [10, 20]}


def test_delete_from_nested_list_dict():
    d = {"a": [{"b": 1}, {"b": 2}]}
    val = del_path(d, "a.0.b")
    assert val == 1
    assert d == {"a": [{}, {"b": 2}]} or d == {"a": [{}, {"b": 2}]}  # acceptable depending on dict emptiness


# --------------------------------------------------------------
# ERROR CASES
# --------------------------------------------------------------

def test_set_list_index_non_integer():
    d = {"a": [1]}
    with pytest.raises(PathError):
        set_path(d, "a.x", 1)


def test_replace_list_with_dict_key():
    """Setting dict key where list exists"""
    d = {"a": [1, 2, 3]}
    # This should fail - can't navigate dict key into a list
    with pytest.raises(PathError):
        set_path(d, "a.notanumber", 5)


def test_get_list_index_non_integer():
    d = {"a": [1]}
    assert get_path(d, "a.x") is None  # default


def test_delete_non_integer_list_index():
    d = {"a": [1]}
    with pytest.raises(PathError):
        del_path(d, "a.x", allow_list_mutation=True)


def test_set_path_invalid_type():
    d = {"a": 1}
    with pytest.raises(PathError):
        set_path(d, "a.b", 10)


def test_delete_path_invalid_type():
    d = {"a": 5}
    with pytest.raises(PathError):
        del_path(d, "a.b")


def test_empty_string_path():
    """Empty path should be handled gracefully"""
    d = {"a": 1}
    with pytest.raises(PathError):
        set_path(d, "", 5)


def test_get_empty_path():
    """Get with empty path"""
    d = {"a": 1}
    result = get_path(d, "")
    # This behavior needs to be defined


# --------------------------------------------------------------
# INVALID PATH TYPE TESTS
# --------------------------------------------------------------

def test_get_path_invalid_type_int():
    """get_path should raise PathError with INVALID_PATH code for invalid path types"""
    d = {"a": 1}
    with pytest.raises(PathError) as exc_info:
        get_path(d, 123)
    assert exc_info.value.code == PathErrorCode.INVALID_PATH


def test_get_path_invalid_type_none():
    """get_path should raise PathError for None path"""
    d = {"a": 1}
    with pytest.raises(PathError) as exc_info:
        get_path(d, None)
    assert exc_info.value.code == PathErrorCode.INVALID_PATH


def test_get_path_invalid_type_dict():
    """get_path should raise PathError for dict path"""
    d = {"a": 1}
    with pytest.raises(PathError) as exc_info:
        get_path(d, {"key": "value"})
    assert exc_info.value.code == PathErrorCode.INVALID_PATH


def test_get_path_invalid_type_tuple():
    """get_path should raise PathError for tuple path"""
    d = {"a": 1}
    with pytest.raises(PathError) as exc_info:
        get_path(d, ("a", "b"))
    assert exc_info.value.code == PathErrorCode.INVALID_PATH


def test_set_path_invalid_type_int():
    """set_path should raise PathError with INVALID_PATH code for invalid path types"""
    d = {}
    with pytest.raises(PathError) as exc_info:
        set_path(d, 42, "value")
    assert exc_info.value.code == PathErrorCode.INVALID_PATH


def test_set_path_invalid_type_none():
    """set_path should raise PathError for None path"""
    d = {}
    with pytest.raises(PathError) as exc_info:
        set_path(d, None, "value")
    assert exc_info.value.code == PathErrorCode.INVALID_PATH


def test_set_path_invalid_type_dict():
    """set_path should raise PathError for dict path"""
    d = {}
    with pytest.raises(PathError) as exc_info:
        set_path(d, {"key": "value"}, "value")
    assert exc_info.value.code == PathErrorCode.INVALID_PATH


def test_del_path_invalid_type_int():
    """del_path should raise PathError with INVALID_PATH code for invalid path types"""
    d = {"a": 1}
    with pytest.raises(PathError) as exc_info:
        del_path(d, 123)
    assert exc_info.value.code == PathErrorCode.INVALID_PATH


def test_del_path_invalid_type_none():
    """del_path should raise PathError for None path"""
    d = {"a": 1}
    with pytest.raises(PathError) as exc_info:
        del_path(d, None)
    assert exc_info.value.code == PathErrorCode.INVALID_PATH


def test_del_path_invalid_type_tuple():
    """del_path should raise PathError for tuple path"""
    d = {"a": 1}
    with pytest.raises(PathError) as exc_info:
        del_path(d, ("a", "b"))
    assert exc_info.value.code == PathErrorCode.INVALID_PATH


def test_all_functions_raise_path_error_for_invalid_types():
    """Verify all functions consistently raise PathError for invalid path types"""
    d = {"a": 1}
    invalid_paths = [123, None, {}, tuple(), set(), 3.14, True]
    
    for invalid_path in invalid_paths:
        # Test get_path
        with pytest.raises(PathError) as exc_info:
            get_path(d, invalid_path)
        assert exc_info.value.code == PathErrorCode.INVALID_PATH
        
        # Test set_path
        with pytest.raises(PathError) as exc_info:
            set_path(d, invalid_path, "value")
        assert exc_info.value.code == PathErrorCode.INVALID_PATH
        
        # Test del_path
        with pytest.raises(PathError) as exc_info:
            del_path(d, invalid_path)
        assert exc_info.value.code == PathErrorCode.INVALID_PATH


def test_set_negative_index_on_empty_dict():
    """Can't create list with negative index as first operation"""
    d = {}
    # This should probably fail - can't determine list length from negative index
    with pytest.raises((PathError, IndexError)):
        set_path(d, "a.-1", 5)


def test_numeric_key_on_existing_dict():
    """Setting numeric key on existing dict creates string key"""
    d = {"a": {"b": 1}}
    # Numeric keys on dicts are treated as string keys - flexible behavior
    set_path(d, "a.0", 5)
    assert d == {"a": {"b": 1, "0": 5}}


def test_invalid_negative_format():
    """String starting with - but not a valid negative number"""
    d = {}
    set_path(d, "a.-5x", 1)
    assert d == {"a": {"-5x": 1}}  # Should be dict key


def test_just_minus_sign():
    """Just a minus sign should be dict key"""
    d = {}
    set_path(d, "a.-", 1)
    assert d == {"a": {"-": 1}}


def test_multiple_minus_signs():
    """Multiple minus signs"""
    d = {}
    set_path(d, "a.--5", 1)
    assert d == {"a": {"--5": 1}}


# --------------------------------------------------------------
# PATH NORMALIZATION
# --------------------------------------------------------------

def test_path_as_list_form():
    d = {"a": {"b": {"c": 1}}}
    assert get_path(d, ["a", "b", "c"]) == 1


def test_path_list_mixed_int():
    d = {"a": [{"b": 3}]}
    assert get_path(d, ["a", 0, "b"]) == 3


def test_keys_with_dots_in_list_form():
    """Using list form allows keys with dots"""
    d = {}
    set_path(d, ["a.b", "c.d"], 10)
    assert d == {"a.b": {"c.d": 10}}


def test_unicode_keys():
    """Unicode in keys should work"""
    d = {}
    set_path(d, "你好.world.🌍", 42)
    assert get_path(d, "你好.world.🌍") == 42


# --------------------------------------------------------------
# COMPLEX CASES
# --------------------------------------------------------------

def test_set_deep_mixed_structure():
    d = {}
    set_path(d, "x.0.y.1.z", 42)
    assert d == {
        "x": [
            {
                "y": [
                    None,
                    {"z": 42}
                ]
            }
        ]
    }


def test_get_after_set_symmetric():
    d = {}
    set_path(d, "a.0.b.0.c", "X")
    assert get_path(d, "a.0.b.0.c") == "X"


def test_delete_leaf_inside_nested_mixed():
    d = {"x": [{"y": {"z": 5}}]}
    val = del_path(d, "x.0.y.z")
    assert val == 5
    assert d == {"x": [{"y": {}}]}


def test_delete_complex_list_item():
    d = {"a": [{"b": 1}, {"b": 2}, {"b": 3}]}
    del_path(d, "a.1", allow_list_mutation=True)
    assert d == {"a": [{"b": 1}, {"b": 3}]}


def test_set_path_creates_correct_types_auto():
    d = {}
    set_path(d, "root.0.child.0", 10)
    assert d == {"root": [{"child": [10]}]}


def test_overwrite_value_with_container():
    """Overwrite a value then navigate into it"""
    d = {"a": 5}
    # First this should work
    set_path(d, "a", {"b": 1})
    assert d == {"a": {"b": 1}}
    # Then this should work
    set_path(d, "a.c", 2)
    assert d == {"a": {"b": 1, "c": 2}}


def test_final_key_extends_list():
    """Final key extending list should always fill with None"""
    d = {"a": []}
    set_path(d, "a.5", 99)
    assert d == {"a": [None, None, None, None, None, 99]}


def test_very_large_sparse_list():
    """Creating very large sparse list should work but might be slow"""
    d = {}
    set_path(d, "a.1000", 1)
    assert len(d["a"]) == 1001
    assert d["a"][1000] == 1
