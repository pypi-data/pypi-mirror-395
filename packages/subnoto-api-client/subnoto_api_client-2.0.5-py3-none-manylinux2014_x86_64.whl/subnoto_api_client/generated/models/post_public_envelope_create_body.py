from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="PostPublicEnvelopeCreateBody")



@_attrs_define
class PostPublicEnvelopeCreateBody:
    """ 
        Attributes:
            workspace_uuid (str): The UUID of the workspace to create the envelope in.
            envelope_title (str): The title of the envelope being created.
            file (str | Unset): Base64-encoded PDF file data (max 10 MB). If provided, the file will be encrypted and
                uploaded directly, and presignedS3Params will not be returned.
     """

    workspace_uuid: str
    envelope_title: str
    file: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        workspace_uuid = self.workspace_uuid

        envelope_title = self.envelope_title

        file = self.file


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "workspaceUuid": workspace_uuid,
            "envelopeTitle": envelope_title,
        })
        if file is not UNSET:
            field_dict["file"] = file

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        workspace_uuid = d.pop("workspaceUuid")

        envelope_title = d.pop("envelopeTitle")

        file = d.pop("file", UNSET)

        post_public_envelope_create_body = cls(
            workspace_uuid=workspace_uuid,
            envelope_title=envelope_title,
            file=file,
        )


        post_public_envelope_create_body.additional_properties = d
        return post_public_envelope_create_body

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
