from enum import Enum

class PostPublicContactListResponse400ErrorCode(str, Enum):
    INVALID_REQUEST_FORMAT = "INVALID_REQUEST_FORMAT"
    WORKSPACE_NOT_FOUND = "WORKSPACE_NOT_FOUND"

    def __str__(self) -> str:
        return str(self.value)
