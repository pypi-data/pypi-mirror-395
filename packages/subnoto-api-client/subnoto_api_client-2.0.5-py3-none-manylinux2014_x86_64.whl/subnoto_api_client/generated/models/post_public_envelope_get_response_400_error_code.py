from enum import Enum

class PostPublicEnvelopeGetResponse400ErrorCode(str, Enum):
    ENVELOPE_NOT_FOUND = "ENVELOPE_NOT_FOUND"
    INVALID_REQUEST_FORMAT = "INVALID_REQUEST_FORMAT"
    WORKSPACE_NOT_FOUND = "WORKSPACE_NOT_FOUND"

    def __str__(self) -> str:
        return str(self.value)
