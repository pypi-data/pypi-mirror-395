from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.post_public_envelope_add_recipients_response_200_recipients_item_role import PostPublicEnvelopeAddRecipientsResponse200RecipientsItemRole
from ..models.post_public_envelope_add_recipients_response_200_recipients_item_status import PostPublicEnvelopeAddRecipientsResponse200RecipientsItemStatus






T = TypeVar("T", bound="PostPublicEnvelopeAddRecipientsResponse200RecipientsItem")



@_attrs_define
class PostPublicEnvelopeAddRecipientsResponse200RecipientsItem:
    """ 
        Attributes:
            email (str): The recipient's email address.
            firstname (str): The recipient's first name.
            lastname (str): The recipient's last name.
            role (PostPublicEnvelopeAddRecipientsResponse200RecipientsItemRole): The recipient's role.
            associated_contact (bool): Whether the recipient is associated with a contact.
            status (PostPublicEnvelopeAddRecipientsResponse200RecipientsItemStatus): The current status of the recipient.
     """

    email: str
    firstname: str
    lastname: str
    role: PostPublicEnvelopeAddRecipientsResponse200RecipientsItemRole
    associated_contact: bool
    status: PostPublicEnvelopeAddRecipientsResponse200RecipientsItemStatus





    def to_dict(self) -> dict[str, Any]:
        email = self.email

        firstname = self.firstname

        lastname = self.lastname

        role = self.role.value

        associated_contact = self.associated_contact

        status = self.status.value


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "email": email,
            "firstname": firstname,
            "lastname": lastname,
            "role": role,
            "associatedContact": associated_contact,
            "status": status,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        email = d.pop("email")

        firstname = d.pop("firstname")

        lastname = d.pop("lastname")

        role = PostPublicEnvelopeAddRecipientsResponse200RecipientsItemRole(d.pop("role"))




        associated_contact = d.pop("associatedContact")

        status = PostPublicEnvelopeAddRecipientsResponse200RecipientsItemStatus(d.pop("status"))




        post_public_envelope_add_recipients_response_200_recipients_item = cls(
            email=email,
            firstname=firstname,
            lastname=lastname,
            role=role,
            associated_contact=associated_contact,
            status=status,
        )

        return post_public_envelope_add_recipients_response_200_recipients_item

