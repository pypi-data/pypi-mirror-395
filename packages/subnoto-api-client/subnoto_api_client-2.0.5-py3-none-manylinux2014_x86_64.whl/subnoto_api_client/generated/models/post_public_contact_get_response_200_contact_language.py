from enum import Enum

class PostPublicContactGetResponse200ContactLanguage(str, Enum):
    EN = "en"
    FR = "fr"

    def __str__(self) -> str:
        return str(self.value)
