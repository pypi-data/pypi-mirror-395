from enum import Enum

class PostPublicEnvelopeAddRecipientsBodyRecipientsItemType0VerificationType(str, Enum):
    NONE = "none"
    SMS = "sms"

    def __str__(self) -> str:
        return str(self.value)
