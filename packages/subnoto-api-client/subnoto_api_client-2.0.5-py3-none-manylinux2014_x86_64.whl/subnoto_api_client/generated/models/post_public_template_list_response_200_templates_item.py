from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.post_public_template_list_response_200_templates_item_status import PostPublicTemplateListResponse200TemplatesItemStatus
from typing import cast

if TYPE_CHECKING:
  from ..models.post_public_template_list_response_200_templates_item_documents_item import PostPublicTemplateListResponse200TemplatesItemDocumentsItem
  from ..models.post_public_template_list_response_200_templates_item_owner import PostPublicTemplateListResponse200TemplatesItemOwner
  from ..models.post_public_template_list_response_200_templates_item_recipients_item import PostPublicTemplateListResponse200TemplatesItemRecipientsItem





T = TypeVar("T", bound="PostPublicTemplateListResponse200TemplatesItem")



@_attrs_define
class PostPublicTemplateListResponse200TemplatesItem:
    """ 
        Attributes:
            uuid (str): The unique identifier of the template.
            title (str): The title of the template.
            creation_date (float): The date and time the template was created (unix timestamp).
            update_date (float): The date and time the template was last updated (unix timestamp).
            status (PostPublicTemplateListResponse200TemplatesItemStatus): The status of the template.
            workspace_uuid (str): The UUID of the workspace the template belongs to.
            owner (PostPublicTemplateListResponse200TemplatesItemOwner): The creator of the template.
            documents (list[PostPublicTemplateListResponse200TemplatesItemDocumentsItem]):
            tags (list[str]): The tags of the template.
            recipients (list[PostPublicTemplateListResponse200TemplatesItemRecipientsItem]): The recipients of the template.
            recipient_count (float): The number of recipients in the template.
     """

    uuid: str
    title: str
    creation_date: float
    update_date: float
    status: PostPublicTemplateListResponse200TemplatesItemStatus
    workspace_uuid: str
    owner: PostPublicTemplateListResponse200TemplatesItemOwner
    documents: list[PostPublicTemplateListResponse200TemplatesItemDocumentsItem]
    tags: list[str]
    recipients: list[PostPublicTemplateListResponse200TemplatesItemRecipientsItem]
    recipient_count: float





    def to_dict(self) -> dict[str, Any]:
        from ..models.post_public_template_list_response_200_templates_item_documents_item import PostPublicTemplateListResponse200TemplatesItemDocumentsItem
        from ..models.post_public_template_list_response_200_templates_item_owner import PostPublicTemplateListResponse200TemplatesItemOwner
        from ..models.post_public_template_list_response_200_templates_item_recipients_item import PostPublicTemplateListResponse200TemplatesItemRecipientsItem
        uuid = self.uuid

        title = self.title

        creation_date = self.creation_date

        update_date = self.update_date

        status = self.status.value

        workspace_uuid = self.workspace_uuid

        owner = self.owner.to_dict()

        documents = []
        for documents_item_data in self.documents:
            documents_item = documents_item_data.to_dict()
            documents.append(documents_item)



        tags = self.tags



        recipients = []
        for recipients_item_data in self.recipients:
            recipients_item = recipients_item_data.to_dict()
            recipients.append(recipients_item)



        recipient_count = self.recipient_count


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "uuid": uuid,
            "title": title,
            "creationDate": creation_date,
            "updateDate": update_date,
            "status": status,
            "workspaceUuid": workspace_uuid,
            "owner": owner,
            "documents": documents,
            "tags": tags,
            "recipients": recipients,
            "recipientCount": recipient_count,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.post_public_template_list_response_200_templates_item_documents_item import PostPublicTemplateListResponse200TemplatesItemDocumentsItem
        from ..models.post_public_template_list_response_200_templates_item_owner import PostPublicTemplateListResponse200TemplatesItemOwner
        from ..models.post_public_template_list_response_200_templates_item_recipients_item import PostPublicTemplateListResponse200TemplatesItemRecipientsItem
        d = dict(src_dict)
        uuid = d.pop("uuid")

        title = d.pop("title")

        creation_date = d.pop("creationDate")

        update_date = d.pop("updateDate")

        status = PostPublicTemplateListResponse200TemplatesItemStatus(d.pop("status"))




        workspace_uuid = d.pop("workspaceUuid")

        owner = PostPublicTemplateListResponse200TemplatesItemOwner.from_dict(d.pop("owner"))




        documents = []
        _documents = d.pop("documents")
        for documents_item_data in (_documents):
            documents_item = PostPublicTemplateListResponse200TemplatesItemDocumentsItem.from_dict(documents_item_data)



            documents.append(documents_item)


        tags = cast(list[str], d.pop("tags"))


        recipients = []
        _recipients = d.pop("recipients")
        for recipients_item_data in (_recipients):
            recipients_item = PostPublicTemplateListResponse200TemplatesItemRecipientsItem.from_dict(recipients_item_data)



            recipients.append(recipients_item)


        recipient_count = d.pop("recipientCount")

        post_public_template_list_response_200_templates_item = cls(
            uuid=uuid,
            title=title,
            creation_date=creation_date,
            update_date=update_date,
            status=status,
            workspace_uuid=workspace_uuid,
            owner=owner,
            documents=documents,
            tags=tags,
            recipients=recipients,
            recipient_count=recipient_count,
        )

        return post_public_template_list_response_200_templates_item

