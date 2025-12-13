from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast






T = TypeVar("T", bound="PostPublicEnvelopeCreateFromTemplateResponse200")



@_attrs_define
class PostPublicEnvelopeCreateFromTemplateResponse200:
    """ 
        Attributes:
            envelope_uuid (str): The UUID of the created envelope.
            document_uuids (list[str]): Array of UUIDs of the created documents.
     """

    envelope_uuid: str
    document_uuids: list[str]





    def to_dict(self) -> dict[str, Any]:
        envelope_uuid = self.envelope_uuid

        document_uuids = self.document_uuids




        field_dict: dict[str, Any] = {}

        field_dict.update({
            "envelopeUuid": envelope_uuid,
            "documentUuids": document_uuids,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        envelope_uuid = d.pop("envelopeUuid")

        document_uuids = cast(list[str], d.pop("documentUuids"))


        post_public_envelope_create_from_template_response_200 = cls(
            envelope_uuid=envelope_uuid,
            document_uuids=document_uuids,
        )

        return post_public_envelope_create_from_template_response_200

