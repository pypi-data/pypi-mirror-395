from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.post_public_envelope_list_response_200_envelopes_item_status import PostPublicEnvelopeListResponse200EnvelopesItemStatus
from typing import cast

if TYPE_CHECKING:
  from ..models.post_public_envelope_list_response_200_envelopes_item_metrics import PostPublicEnvelopeListResponse200EnvelopesItemMetrics
  from ..models.post_public_envelope_list_response_200_envelopes_item_owner import PostPublicEnvelopeListResponse200EnvelopesItemOwner





T = TypeVar("T", bound="PostPublicEnvelopeListResponse200EnvelopesItem")



@_attrs_define
class PostPublicEnvelopeListResponse200EnvelopesItem:
    """ 
        Attributes:
            uuid (str): The unique identifier of the envelope.
            title (str): The title of the envelope.
            creation_date (float): The date and time the envelope was created (unix timestamp).
            update_date (float): The date and time the envelope was last updated (unix timestamp).
            sent_date (float | None): The date and time the envelope was sent (unix timestamp).
            status (PostPublicEnvelopeListResponse200EnvelopesItemStatus): The status of the envelope.
            workspace_uuid (str): The UUID of the workspace the envelope belongs to.
            owner (PostPublicEnvelopeListResponse200EnvelopesItemOwner): The creator of the envelope.
            metrics (PostPublicEnvelopeListResponse200EnvelopesItemMetrics): The metrics of the envelope.
            tags (list[str]): The tags of the envelope.
     """

    uuid: str
    title: str
    creation_date: float
    update_date: float
    sent_date: float | None
    status: PostPublicEnvelopeListResponse200EnvelopesItemStatus
    workspace_uuid: str
    owner: PostPublicEnvelopeListResponse200EnvelopesItemOwner
    metrics: PostPublicEnvelopeListResponse200EnvelopesItemMetrics
    tags: list[str]





    def to_dict(self) -> dict[str, Any]:
        from ..models.post_public_envelope_list_response_200_envelopes_item_metrics import PostPublicEnvelopeListResponse200EnvelopesItemMetrics
        from ..models.post_public_envelope_list_response_200_envelopes_item_owner import PostPublicEnvelopeListResponse200EnvelopesItemOwner
        uuid = self.uuid

        title = self.title

        creation_date = self.creation_date

        update_date = self.update_date

        sent_date: float | None
        sent_date = self.sent_date

        status = self.status.value

        workspace_uuid = self.workspace_uuid

        owner = self.owner.to_dict()

        metrics = self.metrics.to_dict()

        tags = self.tags




        field_dict: dict[str, Any] = {}

        field_dict.update({
            "uuid": uuid,
            "title": title,
            "creationDate": creation_date,
            "updateDate": update_date,
            "sentDate": sent_date,
            "status": status,
            "workspaceUuid": workspace_uuid,
            "owner": owner,
            "metrics": metrics,
            "tags": tags,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.post_public_envelope_list_response_200_envelopes_item_metrics import PostPublicEnvelopeListResponse200EnvelopesItemMetrics
        from ..models.post_public_envelope_list_response_200_envelopes_item_owner import PostPublicEnvelopeListResponse200EnvelopesItemOwner
        d = dict(src_dict)
        uuid = d.pop("uuid")

        title = d.pop("title")

        creation_date = d.pop("creationDate")

        update_date = d.pop("updateDate")

        def _parse_sent_date(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        sent_date = _parse_sent_date(d.pop("sentDate"))


        status = PostPublicEnvelopeListResponse200EnvelopesItemStatus(d.pop("status"))




        workspace_uuid = d.pop("workspaceUuid")

        owner = PostPublicEnvelopeListResponse200EnvelopesItemOwner.from_dict(d.pop("owner"))




        metrics = PostPublicEnvelopeListResponse200EnvelopesItemMetrics.from_dict(d.pop("metrics"))




        tags = cast(list[str], d.pop("tags"))


        post_public_envelope_list_response_200_envelopes_item = cls(
            uuid=uuid,
            title=title,
            creation_date=creation_date,
            update_date=update_date,
            sent_date=sent_date,
            status=status,
            workspace_uuid=workspace_uuid,
            owner=owner,
            metrics=metrics,
            tags=tags,
        )

        return post_public_envelope_list_response_200_envelopes_item

