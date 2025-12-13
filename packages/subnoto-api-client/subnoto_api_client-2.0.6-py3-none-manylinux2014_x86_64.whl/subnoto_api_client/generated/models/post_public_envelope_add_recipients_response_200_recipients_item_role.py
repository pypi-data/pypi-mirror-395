from enum import Enum

class PostPublicEnvelopeAddRecipientsResponse200RecipientsItemRole(str, Enum):
    SIGNER = "signer"

    def __str__(self) -> str:
        return str(self.value)
