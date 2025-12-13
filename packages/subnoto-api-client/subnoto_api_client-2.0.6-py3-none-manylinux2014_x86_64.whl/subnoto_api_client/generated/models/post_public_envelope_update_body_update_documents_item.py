from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="PostPublicEnvelopeUpdateBodyUpdateDocumentsItem")



@_attrs_define
class PostPublicEnvelopeUpdateBodyUpdateDocumentsItem:
    """ 
        Attributes:
            uuid (str): The unique identifier of the document to update.
            title (str | Unset): The new title of the document.
            initials_on_all_pages (bool | Unset): Whether the initials are on all pages.
     """

    uuid: str
    title: str | Unset = UNSET
    initials_on_all_pages: bool | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        uuid = self.uuid

        title = self.title

        initials_on_all_pages = self.initials_on_all_pages


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "uuid": uuid,
        })
        if title is not UNSET:
            field_dict["title"] = title
        if initials_on_all_pages is not UNSET:
            field_dict["initialsOnAllPages"] = initials_on_all_pages

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = d.pop("uuid")

        title = d.pop("title", UNSET)

        initials_on_all_pages = d.pop("initialsOnAllPages", UNSET)

        post_public_envelope_update_body_update_documents_item = cls(
            uuid=uuid,
            title=title,
            initials_on_all_pages=initials_on_all_pages,
        )


        post_public_envelope_update_body_update_documents_item.additional_properties = d
        return post_public_envelope_update_body_update_documents_item

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
