from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast






T = TypeVar("T", bound="PostPublicEnvelopeListResponse200EnvelopesItemOwner")



@_attrs_define
class PostPublicEnvelopeListResponse200EnvelopesItemOwner:
    """ The creator of the envelope.

        Attributes:
            uuid (str): The unique identifier of the owner.
            email (str): The email of the owner.
            firstname (None | str): The first name of the owner.
            lastname (None | str): The last name of the owner.
     """

    uuid: str
    email: str
    firstname: None | str
    lastname: None | str





    def to_dict(self) -> dict[str, Any]:
        uuid = self.uuid

        email = self.email

        firstname: None | str
        firstname = self.firstname

        lastname: None | str
        lastname = self.lastname


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "uuid": uuid,
            "email": email,
            "firstname": firstname,
            "lastname": lastname,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = d.pop("uuid")

        email = d.pop("email")

        def _parse_firstname(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        firstname = _parse_firstname(d.pop("firstname"))


        def _parse_lastname(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        lastname = _parse_lastname(d.pop("lastname"))


        post_public_envelope_list_response_200_envelopes_item_owner = cls(
            uuid=uuid,
            email=email,
            firstname=firstname,
            lastname=lastname,
        )

        return post_public_envelope_list_response_200_envelopes_item_owner

