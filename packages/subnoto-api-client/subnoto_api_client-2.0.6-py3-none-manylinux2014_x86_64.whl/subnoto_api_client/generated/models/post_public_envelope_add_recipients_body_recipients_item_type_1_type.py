from enum import Enum

class PostPublicEnvelopeAddRecipientsBodyRecipientsItemType1Type(str, Enum):
    CONTACT = "contact"

    def __str__(self) -> str:
        return str(self.value)
