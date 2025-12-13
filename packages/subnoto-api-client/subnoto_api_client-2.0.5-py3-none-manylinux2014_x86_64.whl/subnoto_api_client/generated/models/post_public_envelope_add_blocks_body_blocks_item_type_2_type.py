from enum import Enum

class PostPublicEnvelopeAddBlocksBodyBlocksItemType2Type(str, Enum):
    SIGNATURE = "signature"

    def __str__(self) -> str:
        return str(self.value)
