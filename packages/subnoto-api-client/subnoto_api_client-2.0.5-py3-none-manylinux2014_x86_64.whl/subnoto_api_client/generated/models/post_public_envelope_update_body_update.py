from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.post_public_envelope_update_body_update_documents_item import PostPublicEnvelopeUpdateBodyUpdateDocumentsItem





T = TypeVar("T", bound="PostPublicEnvelopeUpdateBodyUpdate")



@_attrs_define
class PostPublicEnvelopeUpdateBodyUpdate:
    """ 
        Attributes:
            title (str | Unset): The new title of the envelope.
            documents (list[PostPublicEnvelopeUpdateBodyUpdateDocumentsItem] | Unset):
            tags (list[str] | Unset): The names of the tags to add to the envelope.
            signature_order (bool | Unset): Whether signature order is enabled for this envelope.
     """

    title: str | Unset = UNSET
    documents: list[PostPublicEnvelopeUpdateBodyUpdateDocumentsItem] | Unset = UNSET
    tags: list[str] | Unset = UNSET
    signature_order: bool | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.post_public_envelope_update_body_update_documents_item import PostPublicEnvelopeUpdateBodyUpdateDocumentsItem
        title = self.title

        documents: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.documents, Unset):
            documents = []
            for documents_item_data in self.documents:
                documents_item = documents_item_data.to_dict()
                documents.append(documents_item)



        tags: list[str] | Unset = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags



        signature_order = self.signature_order


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if title is not UNSET:
            field_dict["title"] = title
        if documents is not UNSET:
            field_dict["documents"] = documents
        if tags is not UNSET:
            field_dict["tags"] = tags
        if signature_order is not UNSET:
            field_dict["signatureOrder"] = signature_order

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.post_public_envelope_update_body_update_documents_item import PostPublicEnvelopeUpdateBodyUpdateDocumentsItem
        d = dict(src_dict)
        title = d.pop("title", UNSET)

        _documents = d.pop("documents", UNSET)
        documents: list[PostPublicEnvelopeUpdateBodyUpdateDocumentsItem] | Unset = UNSET
        if _documents is not UNSET:
            documents = []
            for documents_item_data in _documents:
                documents_item = PostPublicEnvelopeUpdateBodyUpdateDocumentsItem.from_dict(documents_item_data)



                documents.append(documents_item)


        tags = cast(list[str], d.pop("tags", UNSET))


        signature_order = d.pop("signatureOrder", UNSET)

        post_public_envelope_update_body_update = cls(
            title=title,
            documents=documents,
            tags=tags,
            signature_order=signature_order,
        )


        post_public_envelope_update_body_update.additional_properties = d
        return post_public_envelope_update_body_update

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
