from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.post_public_envelope_add_recipients_body_recipients_item_type_0_language import PostPublicEnvelopeAddRecipientsBodyRecipientsItemType0Language
from ..models.post_public_envelope_add_recipients_body_recipients_item_type_0_type import PostPublicEnvelopeAddRecipientsBodyRecipientsItemType0Type
from ..models.post_public_envelope_add_recipients_body_recipients_item_type_0_verification_type import PostPublicEnvelopeAddRecipientsBodyRecipientsItemType0VerificationType
from ..types import UNSET, Unset






T = TypeVar("T", bound="PostPublicEnvelopeAddRecipientsBodyRecipientsItemType0")



@_attrs_define
class PostPublicEnvelopeAddRecipientsBodyRecipientsItemType0:
    """ 
        Attributes:
            type_ (PostPublicEnvelopeAddRecipientsBodyRecipientsItemType0Type):
            email (str): The recipient's email address.
            firstname (str): The recipient's first name.
            lastname (str): The recipient's last name.
            phone (str | Unset): The recipient's phone number (required for SMS verification).
            language (PostPublicEnvelopeAddRecipientsBodyRecipientsItemType0Language | Unset): The language for the
                recipient (e.g., 'en', 'fr').
            verification_type (PostPublicEnvelopeAddRecipientsBodyRecipientsItemType0VerificationType | Unset): The
                verification type for the recipient.
     """

    type_: PostPublicEnvelopeAddRecipientsBodyRecipientsItemType0Type
    email: str
    firstname: str
    lastname: str
    phone: str | Unset = UNSET
    language: PostPublicEnvelopeAddRecipientsBodyRecipientsItemType0Language | Unset = UNSET
    verification_type: PostPublicEnvelopeAddRecipientsBodyRecipientsItemType0VerificationType | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_.value

        email = self.email

        firstname = self.firstname

        lastname = self.lastname

        phone = self.phone

        language: str | Unset = UNSET
        if not isinstance(self.language, Unset):
            language = self.language.value


        verification_type: str | Unset = UNSET
        if not isinstance(self.verification_type, Unset):
            verification_type = self.verification_type.value



        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "type": type_,
            "email": email,
            "firstname": firstname,
            "lastname": lastname,
        })
        if phone is not UNSET:
            field_dict["phone"] = phone
        if language is not UNSET:
            field_dict["language"] = language
        if verification_type is not UNSET:
            field_dict["verificationType"] = verification_type

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        type_ = PostPublicEnvelopeAddRecipientsBodyRecipientsItemType0Type(d.pop("type"))




        email = d.pop("email")

        firstname = d.pop("firstname")

        lastname = d.pop("lastname")

        phone = d.pop("phone", UNSET)

        _language = d.pop("language", UNSET)
        language: PostPublicEnvelopeAddRecipientsBodyRecipientsItemType0Language | Unset
        if isinstance(_language,  Unset):
            language = UNSET
        else:
            language = PostPublicEnvelopeAddRecipientsBodyRecipientsItemType0Language(_language)




        _verification_type = d.pop("verificationType", UNSET)
        verification_type: PostPublicEnvelopeAddRecipientsBodyRecipientsItemType0VerificationType | Unset
        if isinstance(_verification_type,  Unset):
            verification_type = UNSET
        else:
            verification_type = PostPublicEnvelopeAddRecipientsBodyRecipientsItemType0VerificationType(_verification_type)




        post_public_envelope_add_recipients_body_recipients_item_type_0 = cls(
            type_=type_,
            email=email,
            firstname=firstname,
            lastname=lastname,
            phone=phone,
            language=language,
            verification_type=verification_type,
        )


        post_public_envelope_add_recipients_body_recipients_item_type_0.additional_properties = d
        return post_public_envelope_add_recipients_body_recipients_item_type_0

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
