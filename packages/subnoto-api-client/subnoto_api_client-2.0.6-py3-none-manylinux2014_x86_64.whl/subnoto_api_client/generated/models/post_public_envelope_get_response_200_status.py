from enum import Enum

class PostPublicEnvelopeGetResponse200Status(str, Enum):
    APPROVING = "approving"
    CANCELED = "canceled"
    COMPLETE = "complete"
    DECLINED = "declined"
    DRAFT = "draft"
    SIGNING = "signing"
    UPLOADING = "uploading"

    def __str__(self) -> str:
        return str(self.value)
