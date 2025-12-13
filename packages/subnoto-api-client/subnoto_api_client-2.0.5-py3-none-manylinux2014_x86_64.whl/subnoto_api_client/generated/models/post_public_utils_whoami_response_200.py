from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="PostPublicUtilsWhoamiResponse200")



@_attrs_define
class PostPublicUtilsWhoamiResponse200:
    """ 
        Attributes:
            team_uuid (str): The UUID of the team.
            team_name (str): The name of the team.
            owner_email (str): The email of the owner.
            owner_uuid (str): The UUID of the owner.
            access_key (str): The API key used to authenticate the request.
     """

    team_uuid: str
    team_name: str
    owner_email: str
    owner_uuid: str
    access_key: str





    def to_dict(self) -> dict[str, Any]:
        team_uuid = self.team_uuid

        team_name = self.team_name

        owner_email = self.owner_email

        owner_uuid = self.owner_uuid

        access_key = self.access_key


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "teamUuid": team_uuid,
            "teamName": team_name,
            "ownerEmail": owner_email,
            "ownerUuid": owner_uuid,
            "accessKey": access_key,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        team_uuid = d.pop("teamUuid")

        team_name = d.pop("teamName")

        owner_email = d.pop("ownerEmail")

        owner_uuid = d.pop("ownerUuid")

        access_key = d.pop("accessKey")

        post_public_utils_whoami_response_200 = cls(
            team_uuid=team_uuid,
            team_name=team_name,
            owner_email=owner_email,
            owner_uuid=owner_uuid,
            access_key=access_key,
        )

        return post_public_utils_whoami_response_200

