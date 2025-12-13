from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.post_public_envelope_get_response_200_documents_item_blocks_additional_property_item_type_1 import PostPublicEnvelopeGetResponse200DocumentsItemBlocksAdditionalPropertyItemType1
  from ..models.post_public_envelope_get_response_200_documents_item_blocks_additional_property_item_type_2 import PostPublicEnvelopeGetResponse200DocumentsItemBlocksAdditionalPropertyItemType2
  from ..models.post_public_envelope_get_response_200_documents_item_blocks_additional_property_item_type_0 import PostPublicEnvelopeGetResponse200DocumentsItemBlocksAdditionalPropertyItemType0





T = TypeVar("T", bound="PostPublicEnvelopeGetResponse200DocumentsItemBlocks")



@_attrs_define
class PostPublicEnvelopeGetResponse200DocumentsItemBlocks:
    """ The blocks content of the document organized by page number.

     """

    additional_properties: dict[str, list[PostPublicEnvelopeGetResponse200DocumentsItemBlocksAdditionalPropertyItemType0 | PostPublicEnvelopeGetResponse200DocumentsItemBlocksAdditionalPropertyItemType1 | PostPublicEnvelopeGetResponse200DocumentsItemBlocksAdditionalPropertyItemType2]] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.post_public_envelope_get_response_200_documents_item_blocks_additional_property_item_type_1 import PostPublicEnvelopeGetResponse200DocumentsItemBlocksAdditionalPropertyItemType1
        from ..models.post_public_envelope_get_response_200_documents_item_blocks_additional_property_item_type_2 import PostPublicEnvelopeGetResponse200DocumentsItemBlocksAdditionalPropertyItemType2
        from ..models.post_public_envelope_get_response_200_documents_item_blocks_additional_property_item_type_0 import PostPublicEnvelopeGetResponse200DocumentsItemBlocksAdditionalPropertyItemType0
        
        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = []
            for additional_property_item_data in prop:
                additional_property_item: dict[str, Any]
                if isinstance(additional_property_item_data, PostPublicEnvelopeGetResponse200DocumentsItemBlocksAdditionalPropertyItemType0):
                    additional_property_item = additional_property_item_data.to_dict()
                elif isinstance(additional_property_item_data, PostPublicEnvelopeGetResponse200DocumentsItemBlocksAdditionalPropertyItemType1):
                    additional_property_item = additional_property_item_data.to_dict()
                else:
                    additional_property_item = additional_property_item_data.to_dict()

                field_dict[prop_name].append(additional_property_item)




        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.post_public_envelope_get_response_200_documents_item_blocks_additional_property_item_type_1 import PostPublicEnvelopeGetResponse200DocumentsItemBlocksAdditionalPropertyItemType1
        from ..models.post_public_envelope_get_response_200_documents_item_blocks_additional_property_item_type_2 import PostPublicEnvelopeGetResponse200DocumentsItemBlocksAdditionalPropertyItemType2
        from ..models.post_public_envelope_get_response_200_documents_item_blocks_additional_property_item_type_0 import PostPublicEnvelopeGetResponse200DocumentsItemBlocksAdditionalPropertyItemType0
        d = dict(src_dict)
        post_public_envelope_get_response_200_documents_item_blocks = cls(
        )


        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = []
            _additional_property = prop_dict
            for additional_property_item_data in (_additional_property):
                def _parse_additional_property_item(data: object) -> PostPublicEnvelopeGetResponse200DocumentsItemBlocksAdditionalPropertyItemType0 | PostPublicEnvelopeGetResponse200DocumentsItemBlocksAdditionalPropertyItemType1 | PostPublicEnvelopeGetResponse200DocumentsItemBlocksAdditionalPropertyItemType2:
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        additional_property_item_type_0 = PostPublicEnvelopeGetResponse200DocumentsItemBlocksAdditionalPropertyItemType0.from_dict(data)



                        return additional_property_item_type_0
                    except (TypeError, ValueError, AttributeError, KeyError):
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        additional_property_item_type_1 = PostPublicEnvelopeGetResponse200DocumentsItemBlocksAdditionalPropertyItemType1.from_dict(data)



                        return additional_property_item_type_1
                    except (TypeError, ValueError, AttributeError, KeyError):
                        pass
                    if not isinstance(data, dict):
                        raise TypeError()
                    additional_property_item_type_2 = PostPublicEnvelopeGetResponse200DocumentsItemBlocksAdditionalPropertyItemType2.from_dict(data)



                    return additional_property_item_type_2

                additional_property_item = _parse_additional_property_item(additional_property_item_data)

                additional_property.append(additional_property_item)

            additional_properties[prop_name] = additional_property

        post_public_envelope_get_response_200_documents_item_blocks.additional_properties = additional_properties
        return post_public_envelope_get_response_200_documents_item_blocks

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> list[PostPublicEnvelopeGetResponse200DocumentsItemBlocksAdditionalPropertyItemType0 | PostPublicEnvelopeGetResponse200DocumentsItemBlocksAdditionalPropertyItemType1 | PostPublicEnvelopeGetResponse200DocumentsItemBlocksAdditionalPropertyItemType2]:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: list[PostPublicEnvelopeGetResponse200DocumentsItemBlocksAdditionalPropertyItemType0 | PostPublicEnvelopeGetResponse200DocumentsItemBlocksAdditionalPropertyItemType1 | PostPublicEnvelopeGetResponse200DocumentsItemBlocksAdditionalPropertyItemType2]) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
