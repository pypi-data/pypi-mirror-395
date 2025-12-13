from enum import Enum

class PostPublicContactDeleteResponse400ErrorCode(str, Enum):
    CONTACT_NOT_FOUND = "CONTACT_NOT_FOUND"
    INVALID_REQUEST_FORMAT = "INVALID_REQUEST_FORMAT"
    WORKSPACE_NOT_FOUND = "WORKSPACE_NOT_FOUND"

    def __str__(self) -> str:
        return str(self.value)
