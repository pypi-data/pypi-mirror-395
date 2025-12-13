from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.post_public_envelope_create_from_template_body_recipients_item_type_2_type import PostPublicEnvelopeCreateFromTemplateBodyRecipientsItemType2Type






T = TypeVar("T", bound="PostPublicEnvelopeCreateFromTemplateBodyRecipientsItemType2")



@_attrs_define
class PostPublicEnvelopeCreateFromTemplateBodyRecipientsItemType2:
    """ 
        Attributes:
            type_ (PostPublicEnvelopeCreateFromTemplateBodyRecipientsItemType2Type):
            label (str): The label to map to template recipient labels.
            user_uuid (str): The UUID of the workspace member to use.
     """

    type_: PostPublicEnvelopeCreateFromTemplateBodyRecipientsItemType2Type
    label: str
    user_uuid: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_.value

        label = self.label

        user_uuid = self.user_uuid


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "type": type_,
            "label": label,
            "userUuid": user_uuid,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        type_ = PostPublicEnvelopeCreateFromTemplateBodyRecipientsItemType2Type(d.pop("type"))




        label = d.pop("label")

        user_uuid = d.pop("userUuid")

        post_public_envelope_create_from_template_body_recipients_item_type_2 = cls(
            type_=type_,
            label=label,
            user_uuid=user_uuid,
        )


        post_public_envelope_create_from_template_body_recipients_item_type_2.additional_properties = d
        return post_public_envelope_create_from_template_body_recipients_item_type_2

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
