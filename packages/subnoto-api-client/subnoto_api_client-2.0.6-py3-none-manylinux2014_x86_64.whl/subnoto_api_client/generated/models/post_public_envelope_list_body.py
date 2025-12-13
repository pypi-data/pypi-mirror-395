from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="PostPublicEnvelopeListBody")



@_attrs_define
class PostPublicEnvelopeListBody:
    """ 
        Attributes:
            workspace_uuid (str | Unset): The UUID of the workspace to list the envelopes in.
            tags (list[str] | Unset): Optional array of tag names to filter envelopes by
            page (int | Unset): The page number to retrieve (1-indexed). Defaults to 1. Each page contains up to 50 results.
                Default: 1.
     """

    workspace_uuid: str | Unset = UNSET
    tags: list[str] | Unset = UNSET
    page: int | Unset = 1
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        workspace_uuid = self.workspace_uuid

        tags: list[str] | Unset = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags



        page = self.page


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if workspace_uuid is not UNSET:
            field_dict["workspaceUuid"] = workspace_uuid
        if tags is not UNSET:
            field_dict["tags"] = tags
        if page is not UNSET:
            field_dict["page"] = page

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        workspace_uuid = d.pop("workspaceUuid", UNSET)

        tags = cast(list[str], d.pop("tags", UNSET))


        page = d.pop("page", UNSET)

        post_public_envelope_list_body = cls(
            workspace_uuid=workspace_uuid,
            tags=tags,
            page=page,
        )


        post_public_envelope_list_body.additional_properties = d
        return post_public_envelope_list_body

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
