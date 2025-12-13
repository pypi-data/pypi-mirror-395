from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.post_public_envelope_delete_recipients_body_recipients_item import PostPublicEnvelopeDeleteRecipientsBodyRecipientsItem





T = TypeVar("T", bound="PostPublicEnvelopeDeleteRecipientsBody")



@_attrs_define
class PostPublicEnvelopeDeleteRecipientsBody:
    """ 
        Attributes:
            workspace_uuid (str): The UUID of the workspace.
            envelope_uuid (str): The UUID of the envelope.
            recipients (list[PostPublicEnvelopeDeleteRecipientsBodyRecipientsItem]): List of recipients to delete (max 50).
     """

    workspace_uuid: str
    envelope_uuid: str
    recipients: list[PostPublicEnvelopeDeleteRecipientsBodyRecipientsItem]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.post_public_envelope_delete_recipients_body_recipients_item import PostPublicEnvelopeDeleteRecipientsBodyRecipientsItem
        workspace_uuid = self.workspace_uuid

        envelope_uuid = self.envelope_uuid

        recipients = []
        for recipients_item_data in self.recipients:
            recipients_item = recipients_item_data.to_dict()
            recipients.append(recipients_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "workspaceUuid": workspace_uuid,
            "envelopeUuid": envelope_uuid,
            "recipients": recipients,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.post_public_envelope_delete_recipients_body_recipients_item import PostPublicEnvelopeDeleteRecipientsBodyRecipientsItem
        d = dict(src_dict)
        workspace_uuid = d.pop("workspaceUuid")

        envelope_uuid = d.pop("envelopeUuid")

        recipients = []
        _recipients = d.pop("recipients")
        for recipients_item_data in (_recipients):
            recipients_item = PostPublicEnvelopeDeleteRecipientsBodyRecipientsItem.from_dict(recipients_item_data)



            recipients.append(recipients_item)


        post_public_envelope_delete_recipients_body = cls(
            workspace_uuid=workspace_uuid,
            envelope_uuid=envelope_uuid,
            recipients=recipients,
        )


        post_public_envelope_delete_recipients_body.additional_properties = d
        return post_public_envelope_delete_recipients_body

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
