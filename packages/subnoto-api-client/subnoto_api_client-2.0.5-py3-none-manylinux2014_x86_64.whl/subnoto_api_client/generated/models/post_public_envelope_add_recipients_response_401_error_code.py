from enum import Enum

class PostPublicEnvelopeAddRecipientsResponse401ErrorCode(str, Enum):
    AUTHENTICATION_ERROR = "AUTHENTICATION_ERROR"
    INVALID_REQUEST_FORMAT = "INVALID_REQUEST_FORMAT"
    TUNNEL_ERROR = "TUNNEL_ERROR"

    def __str__(self) -> str:
        return str(self.value)
