from enum import Enum

class PostPublicEnvelopeCreateResponse400ErrorCode(str, Enum):
    FILE_SIZE_EXCEEDED = "FILE_SIZE_EXCEEDED"
    INVALID_FILE_DATA = "INVALID_FILE_DATA"
    INVALID_PDF = "INVALID_PDF"
    INVALID_REQUEST_FORMAT = "INVALID_REQUEST_FORMAT"
    WORKSPACE_NOT_FOUND = "WORKSPACE_NOT_FOUND"

    def __str__(self) -> str:
        return str(self.value)
