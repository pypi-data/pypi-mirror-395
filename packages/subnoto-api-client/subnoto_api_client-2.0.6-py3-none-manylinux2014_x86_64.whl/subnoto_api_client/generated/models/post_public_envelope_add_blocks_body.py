from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.post_public_envelope_add_blocks_body_blocks_item_type_1 import PostPublicEnvelopeAddBlocksBodyBlocksItemType1
  from ..models.post_public_envelope_add_blocks_body_blocks_item_type_2 import PostPublicEnvelopeAddBlocksBodyBlocksItemType2
  from ..models.post_public_envelope_add_blocks_body_blocks_item_type_0 import PostPublicEnvelopeAddBlocksBodyBlocksItemType0





T = TypeVar("T", bound="PostPublicEnvelopeAddBlocksBody")



@_attrs_define
class PostPublicEnvelopeAddBlocksBody:
    """ 
        Attributes:
            workspace_uuid (str): The UUID of the workspace.
            envelope_uuid (str): The UUID of the envelope.
            document_uuid (str): The UUID of the document.
            blocks (list[PostPublicEnvelopeAddBlocksBodyBlocksItemType0 | PostPublicEnvelopeAddBlocksBodyBlocksItemType1 |
                PostPublicEnvelopeAddBlocksBodyBlocksItemType2]): Array of blocks to add to the document.
     """

    workspace_uuid: str
    envelope_uuid: str
    document_uuid: str
    blocks: list[PostPublicEnvelopeAddBlocksBodyBlocksItemType0 | PostPublicEnvelopeAddBlocksBodyBlocksItemType1 | PostPublicEnvelopeAddBlocksBodyBlocksItemType2]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.post_public_envelope_add_blocks_body_blocks_item_type_1 import PostPublicEnvelopeAddBlocksBodyBlocksItemType1
        from ..models.post_public_envelope_add_blocks_body_blocks_item_type_2 import PostPublicEnvelopeAddBlocksBodyBlocksItemType2
        from ..models.post_public_envelope_add_blocks_body_blocks_item_type_0 import PostPublicEnvelopeAddBlocksBodyBlocksItemType0
        workspace_uuid = self.workspace_uuid

        envelope_uuid = self.envelope_uuid

        document_uuid = self.document_uuid

        blocks = []
        for blocks_item_data in self.blocks:
            blocks_item: dict[str, Any]
            if isinstance(blocks_item_data, PostPublicEnvelopeAddBlocksBodyBlocksItemType0):
                blocks_item = blocks_item_data.to_dict()
            elif isinstance(blocks_item_data, PostPublicEnvelopeAddBlocksBodyBlocksItemType1):
                blocks_item = blocks_item_data.to_dict()
            else:
                blocks_item = blocks_item_data.to_dict()

            blocks.append(blocks_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "workspaceUuid": workspace_uuid,
            "envelopeUuid": envelope_uuid,
            "documentUuid": document_uuid,
            "blocks": blocks,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.post_public_envelope_add_blocks_body_blocks_item_type_1 import PostPublicEnvelopeAddBlocksBodyBlocksItemType1
        from ..models.post_public_envelope_add_blocks_body_blocks_item_type_2 import PostPublicEnvelopeAddBlocksBodyBlocksItemType2
        from ..models.post_public_envelope_add_blocks_body_blocks_item_type_0 import PostPublicEnvelopeAddBlocksBodyBlocksItemType0
        d = dict(src_dict)
        workspace_uuid = d.pop("workspaceUuid")

        envelope_uuid = d.pop("envelopeUuid")

        document_uuid = d.pop("documentUuid")

        blocks = []
        _blocks = d.pop("blocks")
        for blocks_item_data in (_blocks):
            def _parse_blocks_item(data: object) -> PostPublicEnvelopeAddBlocksBodyBlocksItemType0 | PostPublicEnvelopeAddBlocksBodyBlocksItemType1 | PostPublicEnvelopeAddBlocksBodyBlocksItemType2:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    blocks_item_type_0 = PostPublicEnvelopeAddBlocksBodyBlocksItemType0.from_dict(data)



                    return blocks_item_type_0
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    blocks_item_type_1 = PostPublicEnvelopeAddBlocksBodyBlocksItemType1.from_dict(data)



                    return blocks_item_type_1
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                blocks_item_type_2 = PostPublicEnvelopeAddBlocksBodyBlocksItemType2.from_dict(data)



                return blocks_item_type_2

            blocks_item = _parse_blocks_item(blocks_item_data)

            blocks.append(blocks_item)


        post_public_envelope_add_blocks_body = cls(
            workspace_uuid=workspace_uuid,
            envelope_uuid=envelope_uuid,
            document_uuid=document_uuid,
            blocks=blocks,
        )


        post_public_envelope_add_blocks_body.additional_properties = d
        return post_public_envelope_add_blocks_body

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
