from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.post_public_envelope_get_response_200_status import PostPublicEnvelopeGetResponse200Status
from typing import cast

if TYPE_CHECKING:
  from ..models.post_public_envelope_get_response_200_metrics import PostPublicEnvelopeGetResponse200Metrics
  from ..models.post_public_envelope_get_response_200_owner import PostPublicEnvelopeGetResponse200Owner
  from ..models.post_public_envelope_get_response_200_documents_item import PostPublicEnvelopeGetResponse200DocumentsItem
  from ..models.post_public_envelope_get_response_200_sender import PostPublicEnvelopeGetResponse200Sender





T = TypeVar("T", bound="PostPublicEnvelopeGetResponse200")



@_attrs_define
class PostPublicEnvelopeGetResponse200:
    """ 
        Attributes:
            uuid (str): The unique identifier of the envelope.
            title (str): The title of the envelope.
            status (PostPublicEnvelopeGetResponse200Status): The status of the envelope.
            creation_date (float): The date and time the envelope was created (unix timestamp).
            update_date (float): The date and time the envelope was last updated (unix timestamp).
            sent_date (float | None): The date and time the envelope was sent (unix timestamp).
            owner (PostPublicEnvelopeGetResponse200Owner): The creator of the envelope.
            sender (PostPublicEnvelopeGetResponse200Sender): Information about the sender of the envelope.
            documents (list[PostPublicEnvelopeGetResponse200DocumentsItem]): The list of documents in the envelope.
            tags (list[str]): The tags of the envelope.
            metrics (PostPublicEnvelopeGetResponse200Metrics):
            signature_order (bool): Whether signature order is enabled for this envelope.
            custom_message (None | str): Custom message to include in invitation emails.
     """

    uuid: str
    title: str
    status: PostPublicEnvelopeGetResponse200Status
    creation_date: float
    update_date: float
    sent_date: float | None
    owner: PostPublicEnvelopeGetResponse200Owner
    sender: PostPublicEnvelopeGetResponse200Sender
    documents: list[PostPublicEnvelopeGetResponse200DocumentsItem]
    tags: list[str]
    metrics: PostPublicEnvelopeGetResponse200Metrics
    signature_order: bool
    custom_message: None | str





    def to_dict(self) -> dict[str, Any]:
        from ..models.post_public_envelope_get_response_200_metrics import PostPublicEnvelopeGetResponse200Metrics
        from ..models.post_public_envelope_get_response_200_owner import PostPublicEnvelopeGetResponse200Owner
        from ..models.post_public_envelope_get_response_200_documents_item import PostPublicEnvelopeGetResponse200DocumentsItem
        from ..models.post_public_envelope_get_response_200_sender import PostPublicEnvelopeGetResponse200Sender
        uuid = self.uuid

        title = self.title

        status = self.status.value

        creation_date = self.creation_date

        update_date = self.update_date

        sent_date: float | None
        sent_date = self.sent_date

        owner = self.owner.to_dict()

        sender = self.sender.to_dict()

        documents = []
        for documents_item_data in self.documents:
            documents_item = documents_item_data.to_dict()
            documents.append(documents_item)



        tags = self.tags



        metrics = self.metrics.to_dict()

        signature_order = self.signature_order

        custom_message: None | str
        custom_message = self.custom_message


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "uuid": uuid,
            "title": title,
            "status": status,
            "creationDate": creation_date,
            "updateDate": update_date,
            "sentDate": sent_date,
            "owner": owner,
            "sender": sender,
            "documents": documents,
            "tags": tags,
            "metrics": metrics,
            "signatureOrder": signature_order,
            "customMessage": custom_message,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.post_public_envelope_get_response_200_metrics import PostPublicEnvelopeGetResponse200Metrics
        from ..models.post_public_envelope_get_response_200_owner import PostPublicEnvelopeGetResponse200Owner
        from ..models.post_public_envelope_get_response_200_documents_item import PostPublicEnvelopeGetResponse200DocumentsItem
        from ..models.post_public_envelope_get_response_200_sender import PostPublicEnvelopeGetResponse200Sender
        d = dict(src_dict)
        uuid = d.pop("uuid")

        title = d.pop("title")

        status = PostPublicEnvelopeGetResponse200Status(d.pop("status"))




        creation_date = d.pop("creationDate")

        update_date = d.pop("updateDate")

        def _parse_sent_date(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        sent_date = _parse_sent_date(d.pop("sentDate"))


        owner = PostPublicEnvelopeGetResponse200Owner.from_dict(d.pop("owner"))




        sender = PostPublicEnvelopeGetResponse200Sender.from_dict(d.pop("sender"))




        documents = []
        _documents = d.pop("documents")
        for documents_item_data in (_documents):
            documents_item = PostPublicEnvelopeGetResponse200DocumentsItem.from_dict(documents_item_data)



            documents.append(documents_item)


        tags = cast(list[str], d.pop("tags"))


        metrics = PostPublicEnvelopeGetResponse200Metrics.from_dict(d.pop("metrics"))




        signature_order = d.pop("signatureOrder")

        def _parse_custom_message(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        custom_message = _parse_custom_message(d.pop("customMessage"))


        post_public_envelope_get_response_200 = cls(
            uuid=uuid,
            title=title,
            status=status,
            creation_date=creation_date,
            update_date=update_date,
            sent_date=sent_date,
            owner=owner,
            sender=sender,
            documents=documents,
            tags=tags,
            metrics=metrics,
            signature_order=signature_order,
            custom_message=custom_message,
        )

        return post_public_envelope_get_response_200

