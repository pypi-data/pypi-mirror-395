from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.post_public_envelope_get_response_200_documents_item_blocks import PostPublicEnvelopeGetResponse200DocumentsItemBlocks





T = TypeVar("T", bound="PostPublicEnvelopeGetResponse200DocumentsItem")



@_attrs_define
class PostPublicEnvelopeGetResponse200DocumentsItem:
    """ 
        Attributes:
            uuid (str): The unique identifier of the document.
            title (str): The title of the document.
            blocks (PostPublicEnvelopeGetResponse200DocumentsItemBlocks): The blocks content of the document organized by
                page number.
            signatures_on_separate_page (bool): Whether signatures are placed on a separate page from the document content.
            initials_on_all_pages (bool): Whether initials are required on all pages of the document.
            page_count (float): The number of pages in the document.
            snapshot_date (float | Unset): The date and time the document snapshot was last updated (unix timestamp).
     """

    uuid: str
    title: str
    blocks: PostPublicEnvelopeGetResponse200DocumentsItemBlocks
    signatures_on_separate_page: bool
    initials_on_all_pages: bool
    page_count: float
    snapshot_date: float | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.post_public_envelope_get_response_200_documents_item_blocks import PostPublicEnvelopeGetResponse200DocumentsItemBlocks
        uuid = self.uuid

        title = self.title

        blocks = self.blocks.to_dict()

        signatures_on_separate_page = self.signatures_on_separate_page

        initials_on_all_pages = self.initials_on_all_pages

        page_count = self.page_count

        snapshot_date = self.snapshot_date


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "uuid": uuid,
            "title": title,
            "blocks": blocks,
            "signaturesOnSeparatePage": signatures_on_separate_page,
            "initialsOnAllPages": initials_on_all_pages,
            "pageCount": page_count,
        })
        if snapshot_date is not UNSET:
            field_dict["snapshotDate"] = snapshot_date

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.post_public_envelope_get_response_200_documents_item_blocks import PostPublicEnvelopeGetResponse200DocumentsItemBlocks
        d = dict(src_dict)
        uuid = d.pop("uuid")

        title = d.pop("title")

        blocks = PostPublicEnvelopeGetResponse200DocumentsItemBlocks.from_dict(d.pop("blocks"))




        signatures_on_separate_page = d.pop("signaturesOnSeparatePage")

        initials_on_all_pages = d.pop("initialsOnAllPages")

        page_count = d.pop("pageCount")

        snapshot_date = d.pop("snapshotDate", UNSET)

        post_public_envelope_get_response_200_documents_item = cls(
            uuid=uuid,
            title=title,
            blocks=blocks,
            signatures_on_separate_page=signatures_on_separate_page,
            initials_on_all_pages=initials_on_all_pages,
            page_count=page_count,
            snapshot_date=snapshot_date,
        )

        return post_public_envelope_get_response_200_documents_item

