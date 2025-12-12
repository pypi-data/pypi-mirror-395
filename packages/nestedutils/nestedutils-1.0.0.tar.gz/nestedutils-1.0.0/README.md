# Nested Utils

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Tests](https://github.com/ysskrishna/nestedutils/actions/workflows/test.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)
[![PyPI](https://img.shields.io/pypi/v/nestedutils)](https://pypi.org/project/nestedutils/)

A lightweight Python library for safely navigating and manipulating nested data structures (dicts, lists) using simple dot-notation paths. Ideal for JSON APIs, configs, and complex dict/list objects.

## Why nestedutils?

Working with deeply nested data (like JSON API responses) often leads to verbose, error-prone boilerplate:

```python
# The Standard Way: Verbose and hard to read
user_name = None
if data and "users" in data and len(data["users"]) > 0:
    user = data["users"][0]
    if "profile" in user:
        user_name = user["profile"].get("name")

# With nestedutils: Clean, safe, and readable
from nestedutils import get_path

user_name = get_path(data, "users.0.profile.name")
```

## Features

- **Simple Path Syntax**: Use dot-notation strings (`"a.b.c"`) or lists (`["a", "b", "c"]`) to navigate nested structures
- **Mixed Data Types**: Seamlessly work with dictionaries, lists
- **List Index Support**: Access list elements using numeric indices, including negative indices
- **Auto-creation**: Automatically create missing intermediate containers when setting values
- **Flexible Fill Strategies**: Control how missing containers are created with different fill strategies
- **Type Safety**: Comprehensive error handling with descriptive error messages and error codes
- **Zero Dependencies**: Pure Python implementation with no external dependencies

## Use Cases

- **JSON API Responses**: Safely extract values from complex, unpredictable JSON responses without dozens of checks.
- **Configuration Management**: easily read and modify deeply nested settings in configuration dictionaries.
- **Data Transformation**: Rapidly remap data from one complex structure to another using `get_path` and `set_path`.

## Installation

```bash
pip install nestedutils
```

## Quick Start

```python
from nestedutils import get_path, set_path, del_path

# Create a nested structure
data = {}

# Set values using dot-notation
set_path(data, "user.name", "John")
set_path(data, "user.age", 30)
set_path(data, "user.hobbies.0", "reading")
set_path(data, "user.hobbies.1", "coding")

# Access values
name = get_path(data, "user.name")  # "John"
age = get_path(data, "user.age")    # 30
first_hobby = get_path(data, "user.hobbies.0")  # "reading"

# Delete values
del_path(data, "user.age")
```

## API Reference

### `get_path(data, path, default=None)`

Retrieve a value from a nested data structure.

**Parameters:**

- `data`: The data structure to navigate (dict, list, tuple, or nested combinations)
- `path`: Path to the value (string with dot notation or list of keys/indices)
- `default`: Value to return if path doesn't exist (default: `None`)

**Returns:** The value at the path, or `default` if not found

**Examples:**

```python
data = {"a": {"b": {"c": 5}}}
get_path(data, "a.b.c")  # 5
get_path(data, "a.b.d", default=99)  # 99

data = {"items": [{"name": "apple"}, {"name": "banana"}]}
get_path(data, "items.1.name")  # "banana"
get_path(data, "items.-1.name")  # "banana" (negative index)
```

### `set_path(data, path, value, fill_strategy="auto")`

Set a value in a nested data structure, creating intermediate containers as needed.

**Parameters:**

- `data`: The data structure to modify (must be mutable: dict or list)
- `path`: Path where to set the value (string with dot notation or list of keys/indices)
- `value`: The value to set
- `fill_strategy`: How to fill missing containers (default: `"auto"`)
  - `"auto"`: Intelligently creates `{}` for dicts, `[]` for lists
  - `"none"`: Fills missing list items with `None`
  - `"dict"`: Always creates dictionaries
  - `"list"`: Always creates lists

**Examples:**

```python
data = {}
set_path(data, "user.profile.name", "Alice")
# Creates: {"user": {"profile": {"name": "Alice"}}}

data = {}
set_path(data, "items.0.name", "Item 1")
# Creates: {"items": [{"name": "Item 1"}]}

data = {}
set_path(data, "items.5", "Item 6", fill_strategy="none")
# Creates: {"items": [None, None, None, None, None, "Item 6"]}
```

### `del_path(data, path, allow_list_mutation=False)`

Delete a value from a nested data structure.

**Parameters:**

- `data`: The data structure to modify
- `path`: Path to the value to delete
- `allow_list_mutation`: If `True`, allows deletion from lists (default: `False`)

**Returns:** The deleted value

**Raises:** `PathError` if the path doesn't exist or deletion is not allowed

**Examples:**

```python
data = {"a": {"b": 1, "c": 2}}
del_path(data, "a.b")  # Returns 1, data becomes {"a": {"c": 2}}

data = {"items": [1, 2, 3]}
del_path(data, "items.1", allow_list_mutation=True)  # Returns 2
# data becomes {"items": [1, 3]}
```

## Error Handling

The library uses `PathError` exceptions with error codes for different failure scenarios:

```python
from nestedutils import PathError, PathErrorCode

try:
    set_path(data, "invalid.path", 1)
except PathError as e:
    print(e.message)  # Error message
    print(e.code)     # Error code (PathErrorCode enum)
```

**Error Codes:**

- `INVALID_PATH`: Invalid path format or type
- `INVALID_INDEX`: Invalid list index
- `MISSING_KEY`: Key doesn't exist in dictionary
- `EMPTY_PATH`: Path is empty
- `IMMUTABLE_CONTAINER`: Attempted to modify a tuple
- `INVALID_FILL_STRATEGY`: Invalid fill strategy value

## Advanced Usage

### Using List Paths

List paths are useful when keys contain dots:

```python
data = {}
set_path(data, ["user.name", "first"], "John")
set_path(data, ["user.name", "last"], "Doe")
# Creates: {"user.name": {"first": "John", "last": "Doe"}}
```

### Negative List Indices

Negative indices work like Python list indexing:

```python
data = {"items": [10, 20, 30]}
get_path(data, "items.-1")  # 30 (last item)
set_path(data, "items.-1", 999)  # Updates last item
```

### Working with Tuples

Tuples are read-only. You can read from them but cannot modify:

```python
data = {"items": (1, 2, 3)}
get_path(data, "items.0")  # 1 (works)
set_path(data, "items.0", 9)  # Raises PathError (tuples are immutable)
```

### Handling None Values

The library can navigate through `None` values when setting:

```python
data = {"a": None}
set_path(data, "a.b.c", 10)
# Replaces None with container: {"a": {"b": {"c": 10}}}
```

## Requirements

- Python 3.8+

## Development

For development setup, building, and contributing, see [DEVELOPMENT.md](https://github.com/ysskrishna/nestedutils/blob/main/DEVELOPMENT.md).

## Changelog

See [CHANGELOG.md](https://github.com/ysskrishna/nestedutils/blob/main/CHANGELOG.md) for a detailed list of changes and version history.

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

If you find this library useful, please consider:

- ⭐ **Starring** the repository on GitHub to help others discover it.
- 💖 **Sponsoring** to support ongoing maintenance and development.

[Become a Sponsor on GitHub](https://github.com/sponsors/ysskrishna) | [Support on Patreon](https://patreon.com/ysskrishna)

## Links

- **PyPI**: https://pypi.org/project/nestedutils/
- **Homepage**: https://github.com/ysskrishna/nestedutils
- **Repository**: https://github.com/ysskrishna/nestedutils.git
- **Issues**: https://github.com/ysskrishna/nestedutils/issues

## Author

**Y. Siva Sai Krishna**

- GitHub: [@ysskrishna](https://github.com/ysskrishna)
- LinkedIn: [ysskrishna](https://linkedin.com/in/ysskrishna)
