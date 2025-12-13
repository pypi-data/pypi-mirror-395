from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="PostPublicEnvelopeUpdateResponse200")



@_attrs_define
class PostPublicEnvelopeUpdateResponse200:
    """ 
        Attributes:
            update_date (float): The date and time the envelope was last updated (unix timestamp).
     """

    update_date: float





    def to_dict(self) -> dict[str, Any]:
        update_date = self.update_date


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "updateDate": update_date,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        update_date = d.pop("updateDate")

        post_public_envelope_update_response_200 = cls(
            update_date=update_date,
        )

        return post_public_envelope_update_response_200

