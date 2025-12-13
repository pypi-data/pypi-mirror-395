from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.post_public_envelope_list_response_200_envelopes_item import PostPublicEnvelopeListResponse200EnvelopesItem





T = TypeVar("T", bound="PostPublicEnvelopeListResponse200")



@_attrs_define
class PostPublicEnvelopeListResponse200:
    """ 
        Attributes:
            envelopes (list[PostPublicEnvelopeListResponse200EnvelopesItem]):
     """

    envelopes: list[PostPublicEnvelopeListResponse200EnvelopesItem]





    def to_dict(self) -> dict[str, Any]:
        from ..models.post_public_envelope_list_response_200_envelopes_item import PostPublicEnvelopeListResponse200EnvelopesItem
        envelopes = []
        for envelopes_item_data in self.envelopes:
            envelopes_item = envelopes_item_data.to_dict()
            envelopes.append(envelopes_item)




        field_dict: dict[str, Any] = {}

        field_dict.update({
            "envelopes": envelopes,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.post_public_envelope_list_response_200_envelopes_item import PostPublicEnvelopeListResponse200EnvelopesItem
        d = dict(src_dict)
        envelopes = []
        _envelopes = d.pop("envelopes")
        for envelopes_item_data in (_envelopes):
            envelopes_item = PostPublicEnvelopeListResponse200EnvelopesItem.from_dict(envelopes_item_data)



            envelopes.append(envelopes_item)


        post_public_envelope_list_response_200 = cls(
            envelopes=envelopes,
        )

        return post_public_envelope_list_response_200

