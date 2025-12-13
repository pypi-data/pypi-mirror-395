from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.post_public_contact_update_body_contact import PostPublicContactUpdateBodyContact





T = TypeVar("T", bound="PostPublicContactUpdateBody")



@_attrs_define
class PostPublicContactUpdateBody:
    """ 
        Attributes:
            workspace_uuid (str): The UUID of the workspace to create the envelope in.
            contact (PostPublicContactUpdateBodyContact):
     """

    workspace_uuid: str
    contact: PostPublicContactUpdateBodyContact
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.post_public_contact_update_body_contact import PostPublicContactUpdateBodyContact
        workspace_uuid = self.workspace_uuid

        contact = self.contact.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "workspaceUuid": workspace_uuid,
            "contact": contact,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.post_public_contact_update_body_contact import PostPublicContactUpdateBodyContact
        d = dict(src_dict)
        workspace_uuid = d.pop("workspaceUuid")

        contact = PostPublicContactUpdateBodyContact.from_dict(d.pop("contact"))




        post_public_contact_update_body = cls(
            workspace_uuid=workspace_uuid,
            contact=contact,
        )


        post_public_contact_update_body.additional_properties = d
        return post_public_contact_update_body

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
