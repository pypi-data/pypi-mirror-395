from typing import Any, Union, List
from .exceptions import PathError, PathErrorCode

def _normalize(path):
    if isinstance(path, list):
        return [str(x) for x in path]
    if isinstance(path, str):
        return path.split(".")
    raise PathError(f"path must be string or list, got {type(path).__name__}", PathErrorCode.INVALID_PATH)


def _is_int_key(key):
    if key.startswith("-") and key[1:].isdigit():
        return True
    return key.isdigit()


def _get_list_index(container, key: str):
    """Convert key to index (supports negative indices)."""
    try:
        index = int(key)
    except ValueError:
        raise PathError(f"Invalid list index: {key}", PathErrorCode.INVALID_INDEX)

    if index < 0:
        index = len(container) + index
    return index


def _navigate(container, key, default_marker):
    """Unified navigation for dict/list/tuple."""
    if isinstance(container, dict):
        return container.get(key, default_marker)

    if isinstance(container, (list, tuple)):
        if not _is_int_key(key):
            return default_marker
        idx = _get_list_index(container, key)
        if 0 <= idx < len(container):
            return container[idx]
        return default_marker

    return default_marker


def get_path(data: Any, path: Union[str, list], default=None) -> Any:
    keys = _normalize(path)
    current = data
    MISSING = object()

    for key in keys:
        current = _navigate(current, key, MISSING)
        if current is MISSING:
            return default
    return current


def set_path(
    data: Any,
    path: Union[str, list],
    value: Any,
    fill_strategy="auto"
):
    """
    fill_strategy:
      - "auto": {} for dicts, [] for lists, None for sparse list items
      - "none": fill missing list items with None
      - "dict": always fill with {}
      - "list": always fill with []
    """
    # Validate fill_strategy
    valid_strategies = {"auto", "none", "dict", "list"}
    if fill_strategy not in valid_strategies:
        raise PathError(f"Invalid fill_strategy: {fill_strategy}. Must be one of {valid_strategies}", PathErrorCode.INVALID_FILL_STRATEGY)

    keys = _normalize(path)
    
    # Validate path is not empty
    if not keys or (len(keys) == 1 and keys[0] == ""):
        raise PathError("Path cannot be empty", PathErrorCode.EMPTY_PATH)
    
    current = data

    for i, key in enumerate(keys[:-1]):
        next_key = keys[i + 1]

        # dict case
        if isinstance(current, dict):
            if key not in current:
                if fill_strategy == "dict":
                    current[key] = {}
                elif fill_strategy == "list":
                    current[key] = []
                else:  # auto or none - both intelligently create containers
                    current[key] = [] if _is_int_key(next_key) else {}
            elif current[key] is None:
                # Replace None with appropriate container when navigating deeper
                if fill_strategy == "dict":
                    current[key] = {}
                elif fill_strategy == "list":
                    current[key] = []
                else:  # auto or none
                    current[key] = [] if _is_int_key(next_key) else {}
            current = current[key]
            continue

        # list case
        if isinstance(current, list):
            if not _is_int_key(key):
                raise PathError(f"Expected index at '{key}'", PathErrorCode.INVALID_INDEX)
            idx = _get_list_index(current, key)

            # Fill gaps before the target index
            while len(current) < idx:
                if fill_strategy == "dict":
                    current.append({})
                elif fill_strategy == "list":
                    current.append([])
                else:
                    # auto or none - fill sparse list items with None
                    current.append(None)
            
            # Now create the container at the target index if needed
            if len(current) == idx:
                if fill_strategy == "dict":
                    current.append({})
                elif fill_strategy == "list":
                    current.append([])
                else:
                    # auto or none - create container based on next key
                    current.append([] if _is_int_key(next_key) else {})
            elif current[idx] is None:
                # Replace None with appropriate container when navigating deeper
                if fill_strategy == "dict":
                    current[idx] = {}
                elif fill_strategy == "list":
                    current[idx] = []
                else:  # auto or none
                    current[idx] = [] if _is_int_key(next_key) else {}

            current = current[idx]
            continue

        # tuple case = read-only
        if isinstance(current, tuple):
            raise PathError("Cannot modify inside a tuple", PathErrorCode.IMMUTABLE_CONTAINER)

        raise PathError(f"Cannot navigate into type {type(current)} at {key}", PathErrorCode.INVALID_PATH)

    # final key
    last = keys[-1]

    if isinstance(current, dict):
        current[last] = value
        return

    if isinstance(current, list):
        if not _is_int_key(last):
            raise PathError(f"Expected index at '{last}'", PathErrorCode.INVALID_INDEX)
        idx = _get_list_index(current, last)
        while len(current) <= idx:
            current.append(None)
        current[idx] = value
        return

    if isinstance(current, tuple):
        raise PathError("Cannot modify inside a tuple", PathErrorCode.IMMUTABLE_CONTAINER)

    raise PathError("Cannot set value in non-container type", PathErrorCode.INVALID_PATH)


def del_path(data: Any, path: Union[str, list], allow_list_mutation=False):
    keys = _normalize(path)
    current = data

    for key in keys[:-1]:
        if isinstance(current, dict):
            if key not in current:
                raise PathError(f"Missing key {key}", PathErrorCode.MISSING_KEY)
            current = current[key]
        elif isinstance(current, list):
            if not _is_int_key(key):
                raise PathError(f"Invalid index {key}", PathErrorCode.INVALID_INDEX)
            idx = _get_list_index(current, key)
            try:
                current = current[idx]
            except IndexError:
                raise PathError(f"Missing index {key}", PathErrorCode.INVALID_INDEX)
        else:
            raise PathError(f"Invalid type in path", PathErrorCode.INVALID_PATH)

    last = keys[-1]

    if isinstance(current, dict):
        if last in current:
            return current.pop(last)
        raise PathError(f"Missing key {last}", PathErrorCode.MISSING_KEY)

    if isinstance(current, list):
        if not allow_list_mutation:
            raise PathError("List deletion is disabled. Pass allow_list_mutation=True.", PathErrorCode.INVALID_PATH)
        idx = _get_list_index(current, last)
        try:
            return current.pop(idx)
        except IndexError:
            raise PathError(f"Missing index {last}", PathErrorCode.INVALID_INDEX)

    raise PathError("Cannot delete from non-container type", PathErrorCode.INVALID_PATH)
