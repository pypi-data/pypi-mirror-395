from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.post_public_envelope_update_body_update import PostPublicEnvelopeUpdateBodyUpdate





T = TypeVar("T", bound="PostPublicEnvelopeUpdateBody")



@_attrs_define
class PostPublicEnvelopeUpdateBody:
    """ 
        Attributes:
            workspace_uuid (str): The UUID of the workspace to get the envelope from.
            envelope_uuid (str): The UUID of the envelope to get.
            update (PostPublicEnvelopeUpdateBodyUpdate):
     """

    workspace_uuid: str
    envelope_uuid: str
    update: PostPublicEnvelopeUpdateBodyUpdate
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.post_public_envelope_update_body_update import PostPublicEnvelopeUpdateBodyUpdate
        workspace_uuid = self.workspace_uuid

        envelope_uuid = self.envelope_uuid

        update = self.update.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "workspaceUuid": workspace_uuid,
            "envelopeUuid": envelope_uuid,
            "update": update,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.post_public_envelope_update_body_update import PostPublicEnvelopeUpdateBodyUpdate
        d = dict(src_dict)
        workspace_uuid = d.pop("workspaceUuid")

        envelope_uuid = d.pop("envelopeUuid")

        update = PostPublicEnvelopeUpdateBodyUpdate.from_dict(d.pop("update"))




        post_public_envelope_update_body = cls(
            workspace_uuid=workspace_uuid,
            envelope_uuid=envelope_uuid,
            update=update,
        )


        post_public_envelope_update_body.additional_properties = d
        return post_public_envelope_update_body

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
