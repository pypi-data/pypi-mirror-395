from enum import Enum

class PathErrorCode(Enum):
    INVALID_INDEX = "INVALID_INDEX"
    MISSING_KEY = "MISSING_KEY"
    EMPTY_PATH = "EMPTY_PATH"
    IMMUTABLE_CONTAINER = "IMMUTABLE_CONTAINER"
    INVALID_PATH = "INVALID_PATH"
    INVALID_FILL_STRATEGY = "INVALID_FILL_STRATEGY"


class PathError(Exception):
    """Raised when a nested path cannot be navigated or modified."""
    
    def __init__(self, message: str, code: PathErrorCode = None):
        super().__init__(message)
        self.message = message
        self.code = code
