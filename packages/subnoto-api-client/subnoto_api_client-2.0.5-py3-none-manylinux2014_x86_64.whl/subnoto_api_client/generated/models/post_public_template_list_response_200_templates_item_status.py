from enum import Enum

class PostPublicTemplateListResponse200TemplatesItemStatus(str, Enum):
    ACTIVE = "active"
    ARCHIVED = "archived"
    DRAFT = "draft"
    INCOMPLETE = "incomplete"

    def __str__(self) -> str:
        return str(self.value)
