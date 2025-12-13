from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.post_public_contact_create_response_200_contacts_item import PostPublicContactCreateResponse200ContactsItem





T = TypeVar("T", bound="PostPublicContactCreateResponse200")



@_attrs_define
class PostPublicContactCreateResponse200:
    """ 
        Attributes:
            contacts (list[PostPublicContactCreateResponse200ContactsItem]): The contacts created.
     """

    contacts: list[PostPublicContactCreateResponse200ContactsItem]





    def to_dict(self) -> dict[str, Any]:
        from ..models.post_public_contact_create_response_200_contacts_item import PostPublicContactCreateResponse200ContactsItem
        contacts = []
        for contacts_item_data in self.contacts:
            contacts_item = contacts_item_data.to_dict()
            contacts.append(contacts_item)




        field_dict: dict[str, Any] = {}

        field_dict.update({
            "contacts": contacts,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.post_public_contact_create_response_200_contacts_item import PostPublicContactCreateResponse200ContactsItem
        d = dict(src_dict)
        contacts = []
        _contacts = d.pop("contacts")
        for contacts_item_data in (_contacts):
            contacts_item = PostPublicContactCreateResponse200ContactsItem.from_dict(contacts_item_data)



            contacts.append(contacts_item)


        post_public_contact_create_response_200 = cls(
            contacts=contacts,
        )

        return post_public_contact_create_response_200

