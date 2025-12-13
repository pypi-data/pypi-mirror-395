from enum import Enum

class PostPublicEnvelopeAddBlocksBodyBlocksItemType0TemplatedText(str, Enum):
    EMAIL = "email"
    FULLNAME = "fullname"
    PHONE = "phone"

    def __str__(self) -> str:
        return str(self.value)
