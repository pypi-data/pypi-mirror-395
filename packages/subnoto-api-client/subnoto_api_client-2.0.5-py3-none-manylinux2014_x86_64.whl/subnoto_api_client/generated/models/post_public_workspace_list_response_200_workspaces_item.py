from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="PostPublicWorkspaceListResponse200WorkspacesItem")



@_attrs_define
class PostPublicWorkspaceListResponse200WorkspacesItem:
    """ 
        Attributes:
            uuid (str): The unique identifier of the workspace.
            name (str): The name of the workspace.
            creation_date (float): The date and time the workspace was created (unix timestamp).
            update_date (float): The date and time the workspace was last updated (unix timestamp).
            members_count (float): The number of members in this workspace.
     """

    uuid: str
    name: str
    creation_date: float
    update_date: float
    members_count: float





    def to_dict(self) -> dict[str, Any]:
        uuid = self.uuid

        name = self.name

        creation_date = self.creation_date

        update_date = self.update_date

        members_count = self.members_count


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "uuid": uuid,
            "name": name,
            "creationDate": creation_date,
            "updateDate": update_date,
            "membersCount": members_count,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = d.pop("uuid")

        name = d.pop("name")

        creation_date = d.pop("creationDate")

        update_date = d.pop("updateDate")

        members_count = d.pop("membersCount")

        post_public_workspace_list_response_200_workspaces_item = cls(
            uuid=uuid,
            name=name,
            creation_date=creation_date,
            update_date=update_date,
            members_count=members_count,
        )

        return post_public_workspace_list_response_200_workspaces_item

