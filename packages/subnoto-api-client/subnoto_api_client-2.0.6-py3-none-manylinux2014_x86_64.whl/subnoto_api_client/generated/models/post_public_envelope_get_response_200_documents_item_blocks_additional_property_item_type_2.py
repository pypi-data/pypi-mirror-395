from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.post_public_envelope_get_response_200_documents_item_blocks_additional_property_item_type_2_color import PostPublicEnvelopeGetResponse200DocumentsItemBlocksAdditionalPropertyItemType2Color
from ..models.post_public_envelope_get_response_200_documents_item_blocks_additional_property_item_type_2_label_icon import PostPublicEnvelopeGetResponse200DocumentsItemBlocksAdditionalPropertyItemType2LabelIcon
from ..models.post_public_envelope_get_response_200_documents_item_blocks_additional_property_item_type_2_type import PostPublicEnvelopeGetResponse200DocumentsItemBlocksAdditionalPropertyItemType2Type
from ..types import UNSET, Unset






T = TypeVar("T", bound="PostPublicEnvelopeGetResponse200DocumentsItemBlocksAdditionalPropertyItemType2")



@_attrs_define
class PostPublicEnvelopeGetResponse200DocumentsItemBlocksAdditionalPropertyItemType2:
    """ 
        Attributes:
            uuid (str):
            label (str):
            x (float):
            y (float):
            exportable (bool):
            type_ (PostPublicEnvelopeGetResponse200DocumentsItemBlocksAdditionalPropertyItemType2Type):
            label_icon (PostPublicEnvelopeGetResponse200DocumentsItemBlocksAdditionalPropertyItemType2LabelIcon | Unset):
            height (float | Unset):
            width (float | Unset):
            recipient_email (str | Unset):
            exported (bool | Unset):
            color (PostPublicEnvelopeGetResponse200DocumentsItemBlocksAdditionalPropertyItemType2Color | Unset):
            recipient_label (str | Unset):
     """

    uuid: str
    label: str
    x: float
    y: float
    exportable: bool
    type_: PostPublicEnvelopeGetResponse200DocumentsItemBlocksAdditionalPropertyItemType2Type
    label_icon: PostPublicEnvelopeGetResponse200DocumentsItemBlocksAdditionalPropertyItemType2LabelIcon | Unset = UNSET
    height: float | Unset = UNSET
    width: float | Unset = UNSET
    recipient_email: str | Unset = UNSET
    exported: bool | Unset = UNSET
    color: PostPublicEnvelopeGetResponse200DocumentsItemBlocksAdditionalPropertyItemType2Color | Unset = UNSET
    recipient_label: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        uuid = self.uuid

        label = self.label

        x = self.x

        y = self.y

        exportable = self.exportable

        type_ = self.type_.value

        label_icon: str | Unset = UNSET
        if not isinstance(self.label_icon, Unset):
            label_icon = self.label_icon.value


        height = self.height

        width = self.width

        recipient_email = self.recipient_email

        exported = self.exported

        color: str | Unset = UNSET
        if not isinstance(self.color, Unset):
            color = self.color.value


        recipient_label = self.recipient_label


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "uuid": uuid,
            "label": label,
            "x": x,
            "y": y,
            "exportable": exportable,
            "type": type_,
        })
        if label_icon is not UNSET:
            field_dict["labelIcon"] = label_icon
        if height is not UNSET:
            field_dict["height"] = height
        if width is not UNSET:
            field_dict["width"] = width
        if recipient_email is not UNSET:
            field_dict["recipientEmail"] = recipient_email
        if exported is not UNSET:
            field_dict["exported"] = exported
        if color is not UNSET:
            field_dict["color"] = color
        if recipient_label is not UNSET:
            field_dict["recipientLabel"] = recipient_label

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = d.pop("uuid")

        label = d.pop("label")

        x = d.pop("x")

        y = d.pop("y")

        exportable = d.pop("exportable")

        type_ = PostPublicEnvelopeGetResponse200DocumentsItemBlocksAdditionalPropertyItemType2Type(d.pop("type"))




        _label_icon = d.pop("labelIcon", UNSET)
        label_icon: PostPublicEnvelopeGetResponse200DocumentsItemBlocksAdditionalPropertyItemType2LabelIcon | Unset
        if isinstance(_label_icon,  Unset):
            label_icon = UNSET
        else:
            label_icon = PostPublicEnvelopeGetResponse200DocumentsItemBlocksAdditionalPropertyItemType2LabelIcon(_label_icon)




        height = d.pop("height", UNSET)

        width = d.pop("width", UNSET)

        recipient_email = d.pop("recipientEmail", UNSET)

        exported = d.pop("exported", UNSET)

        _color = d.pop("color", UNSET)
        color: PostPublicEnvelopeGetResponse200DocumentsItemBlocksAdditionalPropertyItemType2Color | Unset
        if isinstance(_color,  Unset):
            color = UNSET
        else:
            color = PostPublicEnvelopeGetResponse200DocumentsItemBlocksAdditionalPropertyItemType2Color(_color)




        recipient_label = d.pop("recipientLabel", UNSET)

        post_public_envelope_get_response_200_documents_item_blocks_additional_property_item_type_2 = cls(
            uuid=uuid,
            label=label,
            x=x,
            y=y,
            exportable=exportable,
            type_=type_,
            label_icon=label_icon,
            height=height,
            width=width,
            recipient_email=recipient_email,
            exported=exported,
            color=color,
            recipient_label=recipient_label,
        )

        return post_public_envelope_get_response_200_documents_item_blocks_additional_property_item_type_2

