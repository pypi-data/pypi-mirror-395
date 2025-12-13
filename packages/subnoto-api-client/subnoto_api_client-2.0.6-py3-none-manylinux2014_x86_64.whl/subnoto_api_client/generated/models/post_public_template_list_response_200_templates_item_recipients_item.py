from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="PostPublicTemplateListResponse200TemplatesItemRecipientsItem")



@_attrs_define
class PostPublicTemplateListResponse200TemplatesItemRecipientsItem:
    """ 
        Attributes:
            label (str): The label of the recipient.
     """

    label: str





    def to_dict(self) -> dict[str, Any]:
        label = self.label


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "label": label,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        label = d.pop("label")

        post_public_template_list_response_200_templates_item_recipients_item = cls(
            label=label,
        )

        return post_public_template_list_response_200_templates_item_recipients_item

