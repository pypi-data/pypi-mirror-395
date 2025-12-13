from enum import Enum

class PostPublicContactUpdateResponse200ContactLanguage(str, Enum):
    EN = "en"
    FR = "fr"

    def __str__(self) -> str:
        return str(self.value)
