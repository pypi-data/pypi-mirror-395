from enum import Enum

class PostPublicEnvelopeDeleteRecipientsResponse400ErrorCode(str, Enum):
    ENVELOPE_NOT_FOUND = "ENVELOPE_NOT_FOUND"
    ENVELOPE_NOT_IN_DRAFT = "ENVELOPE_NOT_IN_DRAFT"
    INVALID_REQUEST_FORMAT = "INVALID_REQUEST_FORMAT"
    RECIPIENT_NOT_FOUND = "RECIPIENT_NOT_FOUND"
    WORKSPACE_NOT_FOUND = "WORKSPACE_NOT_FOUND"

    def __str__(self) -> str:
        return str(self.value)
