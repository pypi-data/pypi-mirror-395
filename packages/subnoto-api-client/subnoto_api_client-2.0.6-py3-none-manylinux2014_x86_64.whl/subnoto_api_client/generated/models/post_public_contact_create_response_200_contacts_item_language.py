from enum import Enum

class PostPublicContactCreateResponse200ContactsItemLanguage(str, Enum):
    EN = "en"
    FR = "fr"

    def __str__(self) -> str:
        return str(self.value)
