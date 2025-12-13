from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.post_public_envelope_add_recipients_body_recipients_item_type_1 import PostPublicEnvelopeAddRecipientsBodyRecipientsItemType1
  from ..models.post_public_envelope_add_recipients_body_recipients_item_type_2 import PostPublicEnvelopeAddRecipientsBodyRecipientsItemType2
  from ..models.post_public_envelope_add_recipients_body_recipients_item_type_0 import PostPublicEnvelopeAddRecipientsBodyRecipientsItemType0





T = TypeVar("T", bound="PostPublicEnvelopeAddRecipientsBody")



@_attrs_define
class PostPublicEnvelopeAddRecipientsBody:
    """ 
        Attributes:
            workspace_uuid (str): The UUID of the workspace.
            envelope_uuid (str): The UUID of the envelope.
            recipients (list[PostPublicEnvelopeAddRecipientsBodyRecipientsItemType0 |
                PostPublicEnvelopeAddRecipientsBodyRecipientsItemType1 |
                PostPublicEnvelopeAddRecipientsBodyRecipientsItemType2]): List of recipients to add (max 50).
     """

    workspace_uuid: str
    envelope_uuid: str
    recipients: list[PostPublicEnvelopeAddRecipientsBodyRecipientsItemType0 | PostPublicEnvelopeAddRecipientsBodyRecipientsItemType1 | PostPublicEnvelopeAddRecipientsBodyRecipientsItemType2]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.post_public_envelope_add_recipients_body_recipients_item_type_1 import PostPublicEnvelopeAddRecipientsBodyRecipientsItemType1
        from ..models.post_public_envelope_add_recipients_body_recipients_item_type_2 import PostPublicEnvelopeAddRecipientsBodyRecipientsItemType2
        from ..models.post_public_envelope_add_recipients_body_recipients_item_type_0 import PostPublicEnvelopeAddRecipientsBodyRecipientsItemType0
        workspace_uuid = self.workspace_uuid

        envelope_uuid = self.envelope_uuid

        recipients = []
        for recipients_item_data in self.recipients:
            recipients_item: dict[str, Any]
            if isinstance(recipients_item_data, PostPublicEnvelopeAddRecipientsBodyRecipientsItemType0):
                recipients_item = recipients_item_data.to_dict()
            elif isinstance(recipients_item_data, PostPublicEnvelopeAddRecipientsBodyRecipientsItemType1):
                recipients_item = recipients_item_data.to_dict()
            else:
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
        from ..models.post_public_envelope_add_recipients_body_recipients_item_type_1 import PostPublicEnvelopeAddRecipientsBodyRecipientsItemType1
        from ..models.post_public_envelope_add_recipients_body_recipients_item_type_2 import PostPublicEnvelopeAddRecipientsBodyRecipientsItemType2
        from ..models.post_public_envelope_add_recipients_body_recipients_item_type_0 import PostPublicEnvelopeAddRecipientsBodyRecipientsItemType0
        d = dict(src_dict)
        workspace_uuid = d.pop("workspaceUuid")

        envelope_uuid = d.pop("envelopeUuid")

        recipients = []
        _recipients = d.pop("recipients")
        for recipients_item_data in (_recipients):
            def _parse_recipients_item(data: object) -> PostPublicEnvelopeAddRecipientsBodyRecipientsItemType0 | PostPublicEnvelopeAddRecipientsBodyRecipientsItemType1 | PostPublicEnvelopeAddRecipientsBodyRecipientsItemType2:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    recipients_item_type_0 = PostPublicEnvelopeAddRecipientsBodyRecipientsItemType0.from_dict(data)



                    return recipients_item_type_0
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    recipients_item_type_1 = PostPublicEnvelopeAddRecipientsBodyRecipientsItemType1.from_dict(data)



                    return recipients_item_type_1
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                recipients_item_type_2 = PostPublicEnvelopeAddRecipientsBodyRecipientsItemType2.from_dict(data)



                return recipients_item_type_2

            recipients_item = _parse_recipients_item(recipients_item_data)

            recipients.append(recipients_item)


        post_public_envelope_add_recipients_body = cls(
            workspace_uuid=workspace_uuid,
            envelope_uuid=envelope_uuid,
            recipients=recipients,
        )


        post_public_envelope_add_recipients_body.additional_properties = d
        return post_public_envelope_add_recipients_body

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
