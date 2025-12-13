from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.post_public_envelope_create_from_template_body_recipients_item_type_1_type import PostPublicEnvelopeCreateFromTemplateBodyRecipientsItemType1Type






T = TypeVar("T", bound="PostPublicEnvelopeCreateFromTemplateBodyRecipientsItemType1")



@_attrs_define
class PostPublicEnvelopeCreateFromTemplateBodyRecipientsItemType1:
    """ 
        Attributes:
            type_ (PostPublicEnvelopeCreateFromTemplateBodyRecipientsItemType1Type):
            label (str): The label to map to template recipient labels.
            contact_uuid (str): The UUID of the contact to use.
     """

    type_: PostPublicEnvelopeCreateFromTemplateBodyRecipientsItemType1Type
    label: str
    contact_uuid: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_.value

        label = self.label

        contact_uuid = self.contact_uuid


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "type": type_,
            "label": label,
            "contactUuid": contact_uuid,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        type_ = PostPublicEnvelopeCreateFromTemplateBodyRecipientsItemType1Type(d.pop("type"))




        label = d.pop("label")

        contact_uuid = d.pop("contactUuid")

        post_public_envelope_create_from_template_body_recipients_item_type_1 = cls(
            type_=type_,
            label=label,
            contact_uuid=contact_uuid,
        )


        post_public_envelope_create_from_template_body_recipients_item_type_1.additional_properties = d
        return post_public_envelope_create_from_template_body_recipients_item_type_1

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
