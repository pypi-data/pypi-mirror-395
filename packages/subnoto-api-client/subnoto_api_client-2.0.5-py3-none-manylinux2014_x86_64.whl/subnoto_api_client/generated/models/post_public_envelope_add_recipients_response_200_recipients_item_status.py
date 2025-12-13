from enum import Enum

class PostPublicEnvelopeAddRecipientsResponse200RecipientsItemStatus(str, Enum):
    APPROVED = "approved"
    CANCELED = "canceled"
    DECLINED = "declined"
    PENDING = "pending"
    SIGNED = "signed"

    def __str__(self) -> str:
        return str(self.value)
