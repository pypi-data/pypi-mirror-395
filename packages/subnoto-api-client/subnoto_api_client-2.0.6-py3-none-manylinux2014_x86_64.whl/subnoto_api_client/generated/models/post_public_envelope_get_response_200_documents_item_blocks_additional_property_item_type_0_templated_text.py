from enum import Enum

class PostPublicEnvelopeGetResponse200DocumentsItemBlocksAdditionalPropertyItemType0TemplatedText(str, Enum):
    ADDRESSLINE1 = "addressLine1"
    ADDRESSLINE2 = "addressLine2"
    CITY = "city"
    COMPANY = "company"
    COUNTRY = "country"
    EMAIL = "email"
    FULLNAME = "fullname"
    JOBTITLE = "jobTitle"
    PHONE = "phone"
    ZIPCODE = "zipCode"

    def __str__(self) -> str:
        return str(self.value)
