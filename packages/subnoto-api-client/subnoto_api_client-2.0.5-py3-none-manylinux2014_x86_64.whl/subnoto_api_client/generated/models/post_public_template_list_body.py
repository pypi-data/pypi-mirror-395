from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="PostPublicTemplateListBody")



@_attrs_define
class PostPublicTemplateListBody:
    """ 
        Attributes:
            workspace_uuid (str | Unset): The UUID of the workspace to list the templates in.
            page (int | Unset): The page number to retrieve (1-indexed). Defaults to 1. Each page contains up to 50 results.
                Default: 1.
     """

    workspace_uuid: str | Unset = UNSET
    page: int | Unset = 1





    def to_dict(self) -> dict[str, Any]:
        workspace_uuid = self.workspace_uuid

        page = self.page


        field_dict: dict[str, Any] = {}

        field_dict.update({
        })
        if workspace_uuid is not UNSET:
            field_dict["workspaceUuid"] = workspace_uuid
        if page is not UNSET:
            field_dict["page"] = page

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        workspace_uuid = d.pop("workspaceUuid", UNSET)

        page = d.pop("page", UNSET)

        post_public_template_list_body = cls(
            workspace_uuid=workspace_uuid,
            page=page,
        )

        return post_public_template_list_body

