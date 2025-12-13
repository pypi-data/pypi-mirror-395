from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="PostPublicEnvelopeSignResponse200")



@_attrs_define
class PostPublicEnvelopeSignResponse200:
    """ 
        Attributes:
            success (bool): Whether the document was successfully signed.
            document_uuid (str): The UUID of the signed document.
            revision_version (float): The version number of the signed document revision.
     """

    success: bool
    document_uuid: str
    revision_version: float





    def to_dict(self) -> dict[str, Any]:
        success = self.success

        document_uuid = self.document_uuid

        revision_version = self.revision_version


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "success": success,
            "documentUuid": document_uuid,
            "revisionVersion": revision_version,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        success = d.pop("success")

        document_uuid = d.pop("documentUuid")

        revision_version = d.pop("revisionVersion")

        post_public_envelope_sign_response_200 = cls(
            success=success,
            document_uuid=document_uuid,
            revision_version=revision_version,
        )

        return post_public_envelope_sign_response_200

