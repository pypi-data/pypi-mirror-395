from enum import Enum

class PostPublicEnvelopeCreateFromTemplateResponse400ErrorCode(str, Enum):
    CONTACT_NOT_FOUND = "CONTACT_NOT_FOUND"
    INVALID_RECIPIENT_LABELS = "INVALID_RECIPIENT_LABELS"
    INVALID_REQUEST_FORMAT = "INVALID_REQUEST_FORMAT"
    TEMPLATE_NOT_FOUND = "TEMPLATE_NOT_FOUND"
    USER_NOT_FOUND = "USER_NOT_FOUND"
    WORKSPACE_NOT_FOUND = "WORKSPACE_NOT_FOUND"

    def __str__(self) -> str:
        return str(self.value)
