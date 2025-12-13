from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="PostPublicEnvelopeGetResponse200Metrics")



@_attrs_define
class PostPublicEnvelopeGetResponse200Metrics:
    """ 
        Attributes:
            signature_count (float): The number of signatures on the envelope.
            signature_required_count (float): The number of signatures required on the envelope.
            approval_count (float): The number of approvals on the envelope.
            approval_required_count (float): The number of approvals required on the envelope.
     """

    signature_count: float
    signature_required_count: float
    approval_count: float
    approval_required_count: float





    def to_dict(self) -> dict[str, Any]:
        signature_count = self.signature_count

        signature_required_count = self.signature_required_count

        approval_count = self.approval_count

        approval_required_count = self.approval_required_count


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "signatureCount": signature_count,
            "signatureRequiredCount": signature_required_count,
            "approvalCount": approval_count,
            "approvalRequiredCount": approval_required_count,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        signature_count = d.pop("signatureCount")

        signature_required_count = d.pop("signatureRequiredCount")

        approval_count = d.pop("approvalCount")

        approval_required_count = d.pop("approvalRequiredCount")

        post_public_envelope_get_response_200_metrics = cls(
            signature_count=signature_count,
            signature_required_count=signature_required_count,
            approval_count=approval_count,
            approval_required_count=approval_required_count,
        )

        return post_public_envelope_get_response_200_metrics

