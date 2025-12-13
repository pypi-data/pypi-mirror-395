from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.post_public_envelope_add_blocks_body_blocks_item_type_2_type import PostPublicEnvelopeAddBlocksBodyBlocksItemType2Type
from ..types import UNSET, Unset






T = TypeVar("T", bound="PostPublicEnvelopeAddBlocksBodyBlocksItemType2")



@_attrs_define
class PostPublicEnvelopeAddBlocksBodyBlocksItemType2:
    """ 
        Attributes:
            page (str): The page number where the block should be placed.
            x (float): The x position of the block on the page.
            y (float): The y position of the block on the page.
            type_ (PostPublicEnvelopeAddBlocksBodyBlocksItemType2Type):
            height (float | Unset): The height of the block.
            width (float | Unset): The width of the block.
            recipient_email (str | Unset): The email of the recipient for templated blocks.
     """

    page: str
    x: float
    y: float
    type_: PostPublicEnvelopeAddBlocksBodyBlocksItemType2Type
    height: float | Unset = UNSET
    width: float | Unset = UNSET
    recipient_email: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        page = self.page

        x = self.x

        y = self.y

        type_ = self.type_.value

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

        type_ = PostPublicEnvelopeAddBlocksBodyBlocksItemType2Type(d.pop("type"))




        height = d.pop("height", UNSET)

        width = d.pop("width", UNSET)

        recipient_email = d.pop("recipientEmail", UNSET)

        post_public_envelope_add_blocks_body_blocks_item_type_2 = cls(
            page=page,
            x=x,
            y=y,
            type_=type_,
            height=height,
            width=width,
            recipient_email=recipient_email,
        )


        post_public_envelope_add_blocks_body_blocks_item_type_2.additional_properties = d
        return post_public_envelope_add_blocks_body_blocks_item_type_2

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
