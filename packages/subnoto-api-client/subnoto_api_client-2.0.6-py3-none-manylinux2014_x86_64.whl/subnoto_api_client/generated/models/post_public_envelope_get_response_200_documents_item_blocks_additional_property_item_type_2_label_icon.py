from enum import Enum

class PostPublicEnvelopeGetResponse200DocumentsItemBlocksAdditionalPropertyItemType2LabelIcon(str, Enum):
    AT = "at"
    BUILDING = "building"
    BUILDING_OFFICE = "building-office"
    CITY = "city"
    IMAGE = "image"
    PHONE = "phone"
    READ_CV_LOGO = "read-cv-logo"
    ROAD_HORIZON = "road-horizon"
    SIGNATURE = "signature"
    TEXT_T = "text-t"
    USER = "user"

    def __str__(self) -> str:
        return str(self.value)
