from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.post_public_envelope_create_from_template_body_recipients_item_type_0 import PostPublicEnvelopeCreateFromTemplateBodyRecipientsItemType0
  from ..models.post_public_envelope_create_from_template_body_recipients_item_type_1 import PostPublicEnvelopeCreateFromTemplateBodyRecipientsItemType1
  from ..models.post_public_envelope_create_from_template_body_recipients_item_type_2 import PostPublicEnvelopeCreateFromTemplateBodyRecipientsItemType2





T = TypeVar("T", bound="PostPublicEnvelopeCreateFromTemplateBody")



@_attrs_define
class PostPublicEnvelopeCreateFromTemplateBody:
    """ 
        Attributes:
            workspace_uuid (str): The UUID of the workspace to create the envelope in.
            template_uuid (str): The UUID of the template to copy from.
            recipients (list[PostPublicEnvelopeCreateFromTemplateBodyRecipientsItemType0 |
                PostPublicEnvelopeCreateFromTemplateBodyRecipientsItemType1 |
                PostPublicEnvelopeCreateFromTemplateBodyRecipientsItemType2]): Array of recipients with labels to map to
                template recipient labels.
     """

    workspace_uuid: str
    template_uuid: str
    recipients: list[PostPublicEnvelopeCreateFromTemplateBodyRecipientsItemType0 | PostPublicEnvelopeCreateFromTemplateBodyRecipientsItemType1 | PostPublicEnvelopeCreateFromTemplateBodyRecipientsItemType2]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.post_public_envelope_create_from_template_body_recipients_item_type_0 import PostPublicEnvelopeCreateFromTemplateBodyRecipientsItemType0
        from ..models.post_public_envelope_create_from_template_body_recipients_item_type_1 import PostPublicEnvelopeCreateFromTemplateBodyRecipientsItemType1
        from ..models.post_public_envelope_create_from_template_body_recipients_item_type_2 import PostPublicEnvelopeCreateFromTemplateBodyRecipientsItemType2
        workspace_uuid = self.workspace_uuid

        template_uuid = self.template_uuid

        recipients = []
        for recipients_item_data in self.recipients:
            recipients_item: dict[str, Any]
            if isinstance(recipients_item_data, PostPublicEnvelopeCreateFromTemplateBodyRecipientsItemType0):
                recipients_item = recipients_item_data.to_dict()
            elif isinstance(recipients_item_data, PostPublicEnvelopeCreateFromTemplateBodyRecipientsItemType1):
                recipients_item = recipients_item_data.to_dict()
            else:
                recipients_item = recipients_item_data.to_dict()

            recipients.append(recipients_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "workspaceUuid": workspace_uuid,
            "templateUuid": template_uuid,
            "recipients": recipients,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.post_public_envelope_create_from_template_body_recipients_item_type_0 import PostPublicEnvelopeCreateFromTemplateBodyRecipientsItemType0
        from ..models.post_public_envelope_create_from_template_body_recipients_item_type_1 import PostPublicEnvelopeCreateFromTemplateBodyRecipientsItemType1
        from ..models.post_public_envelope_create_from_template_body_recipients_item_type_2 import PostPublicEnvelopeCreateFromTemplateBodyRecipientsItemType2
        d = dict(src_dict)
        workspace_uuid = d.pop("workspaceUuid")

        template_uuid = d.pop("templateUuid")

        recipients = []
        _recipients = d.pop("recipients")
        for recipients_item_data in (_recipients):
            def _parse_recipients_item(data: object) -> PostPublicEnvelopeCreateFromTemplateBodyRecipientsItemType0 | PostPublicEnvelopeCreateFromTemplateBodyRecipientsItemType1 | PostPublicEnvelopeCreateFromTemplateBodyRecipientsItemType2:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    recipients_item_type_0 = PostPublicEnvelopeCreateFromTemplateBodyRecipientsItemType0.from_dict(data)



                    return recipients_item_type_0
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    recipients_item_type_1 = PostPublicEnvelopeCreateFromTemplateBodyRecipientsItemType1.from_dict(data)



                    return recipients_item_type_1
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                recipients_item_type_2 = PostPublicEnvelopeCreateFromTemplateBodyRecipientsItemType2.from_dict(data)



                return recipients_item_type_2

            recipients_item = _parse_recipients_item(recipients_item_data)

            recipients.append(recipients_item)


        post_public_envelope_create_from_template_body = cls(
            workspace_uuid=workspace_uuid,
            template_uuid=template_uuid,
            recipients=recipients,
        )


        post_public_envelope_create_from_template_body.additional_properties = d
        return post_public_envelope_create_from_template_body

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
