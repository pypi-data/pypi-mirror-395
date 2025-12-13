from enum import Enum

class PostPublicEnvelopeGetResponse200DocumentsItemBlocksAdditionalPropertyItemType2Color(str, Enum):
    AUXILIARY = "auxiliary"
    DANGER = "danger"
    INFO = "info"
    PRIMARY = "primary"
    SUCCESS = "success"
    WARNING = "warning"

    def __str__(self) -> str:
        return str(self.value)
