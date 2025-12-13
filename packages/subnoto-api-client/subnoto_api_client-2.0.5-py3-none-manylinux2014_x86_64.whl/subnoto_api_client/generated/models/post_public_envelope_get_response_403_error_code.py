from enum import Enum

class PostPublicEnvelopeGetResponse403ErrorCode(str, Enum):
    AUTHORIZATION_ERROR = "AUTHORIZATION_ERROR"
    FEATURE_NOT_IN_CURRENT_PLAN = "FEATURE_NOT_IN_CURRENT_PLAN"
    INVALID_REQUEST_FORMAT = "INVALID_REQUEST_FORMAT"

    def __str__(self) -> str:
        return str(self.value)
