from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="PostPublicEnvelopeAddBlocksResponse200")



@_attrs_define
class PostPublicEnvelopeAddBlocksResponse200:
    """ 
        Attributes:
            snapshot_date (float): The date and time the snapshot was created (unix timestamp).
     """

    snapshot_date: float





    def to_dict(self) -> dict[str, Any]:
        snapshot_date = self.snapshot_date


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "snapshotDate": snapshot_date,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        snapshot_date = d.pop("snapshotDate")

        post_public_envelope_add_blocks_response_200 = cls(
            snapshot_date=snapshot_date,
        )

        return post_public_envelope_add_blocks_response_200

