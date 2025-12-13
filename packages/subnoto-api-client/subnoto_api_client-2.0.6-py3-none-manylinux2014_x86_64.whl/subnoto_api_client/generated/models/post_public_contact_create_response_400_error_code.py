from enum import Enum

class PostPublicContactCreateResponse400ErrorCode(str, Enum):
    CONTACT_EMAIL_ALREADY_EXISTS = "CONTACT_EMAIL_ALREADY_EXISTS"
    INVALID_REQUEST_FORMAT = "INVALID_REQUEST_FORMAT"
    WORKSPACE_NOT_FOUND = "WORKSPACE_NOT_FOUND"

    def __str__(self) -> str:
        return str(self.value)
