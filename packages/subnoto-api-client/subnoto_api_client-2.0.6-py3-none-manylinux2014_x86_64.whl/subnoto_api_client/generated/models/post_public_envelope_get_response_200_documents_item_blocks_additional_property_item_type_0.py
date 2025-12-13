from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.post_public_envelope_get_response_200_documents_item_blocks_additional_property_item_type_0_color import PostPublicEnvelopeGetResponse200DocumentsItemBlocksAdditionalPropertyItemType0Color
from ..models.post_public_envelope_get_response_200_documents_item_blocks_additional_property_item_type_0_label_icon import PostPublicEnvelopeGetResponse200DocumentsItemBlocksAdditionalPropertyItemType0LabelIcon
from ..models.post_public_envelope_get_response_200_documents_item_blocks_additional_property_item_type_0_templated_text import PostPublicEnvelopeGetResponse200DocumentsItemBlocksAdditionalPropertyItemType0TemplatedText
from ..models.post_public_envelope_get_response_200_documents_item_blocks_additional_property_item_type_0_type import PostPublicEnvelopeGetResponse200DocumentsItemBlocksAdditionalPropertyItemType0Type
from ..types import UNSET, Unset






T = TypeVar("T", bound="PostPublicEnvelopeGetResponse200DocumentsItemBlocksAdditionalPropertyItemType0")



@_attrs_define
class PostPublicEnvelopeGetResponse200DocumentsItemBlocksAdditionalPropertyItemType0:
    """ 
        Attributes:
            uuid (str):
            label (str):
            x (float):
            y (float):
            exportable (bool):
            type_ (PostPublicEnvelopeGetResponse200DocumentsItemBlocksAdditionalPropertyItemType0Type):
            text (str):
            label_icon (PostPublicEnvelopeGetResponse200DocumentsItemBlocksAdditionalPropertyItemType0LabelIcon | Unset):
            height (float | Unset):
            width (float | Unset):
            recipient_email (str | Unset):
            exported (bool | Unset):
            color (PostPublicEnvelopeGetResponse200DocumentsItemBlocksAdditionalPropertyItemType0Color | Unset):
            recipient_label (str | Unset):
            templated_text (PostPublicEnvelopeGetResponse200DocumentsItemBlocksAdditionalPropertyItemType0TemplatedText |
                Unset):
            editable (bool | Unset):
     """

    uuid: str
    label: str
    x: float
    y: float
    exportable: bool
    type_: PostPublicEnvelopeGetResponse200DocumentsItemBlocksAdditionalPropertyItemType0Type
    text: str
    label_icon: PostPublicEnvelopeGetResponse200DocumentsItemBlocksAdditionalPropertyItemType0LabelIcon | Unset = UNSET
    height: float | Unset = UNSET
    width: float | Unset = UNSET
    recipient_email: str | Unset = UNSET
    exported: bool | Unset = UNSET
    color: PostPublicEnvelopeGetResponse200DocumentsItemBlocksAdditionalPropertyItemType0Color | Unset = UNSET
    recipient_label: str | Unset = UNSET
    templated_text: PostPublicEnvelopeGetResponse200DocumentsItemBlocksAdditionalPropertyItemType0TemplatedText | Unset = UNSET
    editable: bool | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        uuid = self.uuid

        label = self.label

        x = self.x

        y = self.y

        exportable = self.exportable

        type_ = self.type_.value

        text = self.text

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

        templated_text: str | Unset = UNSET
        if not isinstance(self.templated_text, Unset):
            templated_text = self.templated_text.value


        editable = self.editable


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "uuid": uuid,
            "label": label,
            "x": x,
            "y": y,
            "exportable": exportable,
            "type": type_,
            "text": text,
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
        if templated_text is not UNSET:
            field_dict["templatedText"] = templated_text
        if editable is not UNSET:
            field_dict["editable"] = editable

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = d.pop("uuid")

        label = d.pop("label")

        x = d.pop("x")

        y = d.pop("y")

        exportable = d.pop("exportable")

        type_ = PostPublicEnvelopeGetResponse200DocumentsItemBlocksAdditionalPropertyItemType0Type(d.pop("type"))




        text = d.pop("text")

        _label_icon = d.pop("labelIcon", UNSET)
        label_icon: PostPublicEnvelopeGetResponse200DocumentsItemBlocksAdditionalPropertyItemType0LabelIcon | Unset
        if isinstance(_label_icon,  Unset):
            label_icon = UNSET
        else:
            label_icon = PostPublicEnvelopeGetResponse200DocumentsItemBlocksAdditionalPropertyItemType0LabelIcon(_label_icon)




        height = d.pop("height", UNSET)

        width = d.pop("width", UNSET)

        recipient_email = d.pop("recipientEmail", UNSET)

        exported = d.pop("exported", UNSET)

        _color = d.pop("color", UNSET)
        color: PostPublicEnvelopeGetResponse200DocumentsItemBlocksAdditionalPropertyItemType0Color | Unset
        if isinstance(_color,  Unset):
            color = UNSET
        else:
            color = PostPublicEnvelopeGetResponse200DocumentsItemBlocksAdditionalPropertyItemType0Color(_color)




        recipient_label = d.pop("recipientLabel", UNSET)

        _templated_text = d.pop("templatedText", UNSET)
        templated_text: PostPublicEnvelopeGetResponse200DocumentsItemBlocksAdditionalPropertyItemType0TemplatedText | Unset
        if isinstance(_templated_text,  Unset):
            templated_text = UNSET
        else:
            templated_text = PostPublicEnvelopeGetResponse200DocumentsItemBlocksAdditionalPropertyItemType0TemplatedText(_templated_text)




        editable = d.pop("editable", UNSET)

        post_public_envelope_get_response_200_documents_item_blocks_additional_property_item_type_0 = cls(
            uuid=uuid,
            label=label,
            x=x,
            y=y,
            exportable=exportable,
            type_=type_,
            text=text,
            label_icon=label_icon,
            height=height,
            width=width,
            recipient_email=recipient_email,
            exported=exported,
            color=color,
            recipient_label=recipient_label,
            templated_text=templated_text,
            editable=editable,
        )

        return post_public_envelope_get_response_200_documents_item_blocks_additional_property_item_type_0

