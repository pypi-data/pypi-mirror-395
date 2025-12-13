from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="PostPublicEnvelopeSignBody")



@_attrs_define
class PostPublicEnvelopeSignBody:
    """ 
        Attributes:
            workspace_uuid (str): The UUID of the workspace containing the envelope.
            envelope_uuid (str): The UUID of the envelope containing the document to sign.
            recipient_email (str): The email of the recipient who is signing.
            signature_image (str | Unset): Base64 encoded signature image to be merged with the watermark.
     """

    workspace_uuid: str
    envelope_uuid: str
    recipient_email: str
    signature_image: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        workspace_uuid = self.workspace_uuid

        envelope_uuid = self.envelope_uuid

        recipient_email = self.recipient_email

        signature_image = self.signature_image


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "workspaceUuid": workspace_uuid,
            "envelopeUuid": envelope_uuid,
            "recipientEmail": recipient_email,
        })
        if signature_image is not UNSET:
            field_dict["signatureImage"] = signature_image

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        workspace_uuid = d.pop("workspaceUuid")

        envelope_uuid = d.pop("envelopeUuid")

        recipient_email = d.pop("recipientEmail")

        signature_image = d.pop("signatureImage", UNSET)

        post_public_envelope_sign_body = cls(
            workspace_uuid=workspace_uuid,
            envelope_uuid=envelope_uuid,
            recipient_email=recipient_email,
            signature_image=signature_image,
        )


        post_public_envelope_sign_body.additional_properties = d
        return post_public_envelope_sign_body

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
