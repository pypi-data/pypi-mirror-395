from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.post_public_envelope_add_recipients_response_200_recipients_item import PostPublicEnvelopeAddRecipientsResponse200RecipientsItem





T = TypeVar("T", bound="PostPublicEnvelopeAddRecipientsResponse200")



@_attrs_define
class PostPublicEnvelopeAddRecipientsResponse200:
    """ 
        Attributes:
            recipients (list[PostPublicEnvelopeAddRecipientsResponse200RecipientsItem]):
     """

    recipients: list[PostPublicEnvelopeAddRecipientsResponse200RecipientsItem]





    def to_dict(self) -> dict[str, Any]:
        from ..models.post_public_envelope_add_recipients_response_200_recipients_item import PostPublicEnvelopeAddRecipientsResponse200RecipientsItem
        recipients = []
        for recipients_item_data in self.recipients:
            recipients_item = recipients_item_data.to_dict()
            recipients.append(recipients_item)




        field_dict: dict[str, Any] = {}

        field_dict.update({
            "recipients": recipients,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.post_public_envelope_add_recipients_response_200_recipients_item import PostPublicEnvelopeAddRecipientsResponse200RecipientsItem
        d = dict(src_dict)
        recipients = []
        _recipients = d.pop("recipients")
        for recipients_item_data in (_recipients):
            recipients_item = PostPublicEnvelopeAddRecipientsResponse200RecipientsItem.from_dict(recipients_item_data)



            recipients.append(recipients_item)


        post_public_envelope_add_recipients_response_200 = cls(
            recipients=recipients,
        )

        return post_public_envelope_add_recipients_response_200

