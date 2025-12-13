from enum import Enum

class PostPublicEnvelopeAddRecipientsBodyRecipientsItemType1Language(str, Enum):
    EN = "en"
    FR = "fr"

    def __str__(self) -> str:
        return str(self.value)
