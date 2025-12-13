from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.post_public_envelope_add_blocks_body_blocks_item_type_1_type import PostPublicEnvelopeAddBlocksBodyBlocksItemType1Type
from ..types import UNSET, Unset






T = TypeVar("T", bound="PostPublicEnvelopeAddBlocksBodyBlocksItemType1")



@_attrs_define
class PostPublicEnvelopeAddBlocksBodyBlocksItemType1:
    """ 
        Attributes:
            page (str): The page number where the block should be placed.
            x (float): The x position of the block on the page.
            y (float): The y position of the block on the page.
            type_ (PostPublicEnvelopeAddBlocksBodyBlocksItemType1Type):
            src (str):
            file_type (str): The file type of the image.
            height (float | Unset): The height of the block.
            width (float | Unset): The width of the block.
            recipient_email (str | Unset): The email of the recipient for templated blocks.
     """

    page: str
    x: float
    y: float
    type_: PostPublicEnvelopeAddBlocksBodyBlocksItemType1Type
    src: str
    file_type: str
    height: float | Unset = UNSET
    width: float | Unset = UNSET
    recipient_email: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        page = self.page

        x = self.x

        y = self.y

        type_ = self.type_.value

        src = self.src

        file_type = self.file_type

        height = self.height

        width = self.width

        recipient_email = self.recipient_email


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "page": page,
            "x": x,
            "y": y,
            "type": type_,
            "src": src,
            "fileType": file_type,
        })
        if height is not UNSET:
            field_dict["height"] = height
        if width is not UNSET:
            field_dict["width"] = width
        if recipient_email is not UNSET:
            field_dict["recipientEmail"] = recipient_email

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        page = d.pop("page")

        x = d.pop("x")

        y = d.pop("y")

        type_ = PostPublicEnvelopeAddBlocksBodyBlocksItemType1Type(d.pop("type"))




        src = d.pop("src")

        file_type = d.pop("fileType")

        height = d.pop("height", UNSET)

        width = d.pop("width", UNSET)

        recipient_email = d.pop("recipientEmail", UNSET)

        post_public_envelope_add_blocks_body_blocks_item_type_1 = cls(
            page=page,
            x=x,
            y=y,
            type_=type_,
            src=src,
            file_type=file_type,
            height=height,
            width=width,
            recipient_email=recipient_email,
        )


        post_public_envelope_add_blocks_body_blocks_item_type_1.additional_properties = d
        return post_public_envelope_add_blocks_body_blocks_item_type_1

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
