from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="PostPublicEnvelopeCompleteDocumentUploadBody")



@_attrs_define
class PostPublicEnvelopeCompleteDocumentUploadBody:
    """ 
        Attributes:
            workspace_uuid (str):
            envelope_uuid (str):
            document_uuid (str):
     """

    workspace_uuid: str
    envelope_uuid: str
    document_uuid: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        workspace_uuid = self.workspace_uuid

        envelope_uuid = self.envelope_uuid

        document_uuid = self.document_uuid


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "workspaceUuid": workspace_uuid,
            "envelopeUuid": envelope_uuid,
            "documentUuid": document_uuid,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        workspace_uuid = d.pop("workspaceUuid")

        envelope_uuid = d.pop("envelopeUuid")

        document_uuid = d.pop("documentUuid")

        post_public_envelope_complete_document_upload_body = cls(
            workspace_uuid=workspace_uuid,
            envelope_uuid=envelope_uuid,
            document_uuid=document_uuid,
        )


        post_public_envelope_complete_document_upload_body.additional_properties = d
        return post_public_envelope_complete_document_upload_body

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
