# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.1]

### Added

- GitHub Actions workflow enhancement to automatically create releases on publish

### Changed

- Updated package description for better clarity and discoverability
- Expanded keywords in `pyproject.toml` for improved PyPI searchability
- Updated README with enhanced description and OG image

## [1.0.0]

### Added

- Initial release of nestedutils
- `get_path()` function for accessing nested values in dictionaries, lists
- `set_path()` function for setting nested values with automatic container creation
- `del_path()` function for deleting nested values
- Support for dot-notation string paths (`"a.b.c"`) and list paths (`["a", "b", "c"]`)
- List index support with positive and negative indices
- Multiple fill strategies for `set_path()`:
  - `"auto"`: Intelligently creates containers based on next key type
  - `"none"`: Fills missing list items with `None`
  - `"dict"`: Always creates dictionaries
  - `"list"`: Always creates lists
- Comprehensive error handling with `PathError` exception and `PathErrorCode` enum
- Support for navigating through `None` values (replaces with appropriate containers)
- Sparse list creation when setting values at high indices
- Full test coverage with comprehensive test suite

### Features

- Zero external dependencies
- Python 3.8+ compatibility
- Immutable container protection (tuples cannot be modified)
- Safe list deletion (requires explicit `allow_list_mutation=True` flag)

[1.0.1]: https://github.com/ysskrishna/nestedutils/releases/tag/v1.0.0...v1.0.1
[1.0.0]: https://github.com/ysskrishna/nestedutils/releases/tag/v1.0.0
