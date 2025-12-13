from enum import Enum

class PostPublicEnvelopeAddRecipientsBodyRecipientsItemType1VerificationType(str, Enum):
    NONE = "none"
    SMS = "sms"

    def __str__(self) -> str:
        return str(self.value)
