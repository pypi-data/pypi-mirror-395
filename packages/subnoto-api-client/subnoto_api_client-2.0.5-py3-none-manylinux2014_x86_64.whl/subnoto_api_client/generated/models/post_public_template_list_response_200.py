from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.post_public_template_list_response_200_templates_item import PostPublicTemplateListResponse200TemplatesItem





T = TypeVar("T", bound="PostPublicTemplateListResponse200")



@_attrs_define
class PostPublicTemplateListResponse200:
    """ 
        Attributes:
            templates (list[PostPublicTemplateListResponse200TemplatesItem]):
     """

    templates: list[PostPublicTemplateListResponse200TemplatesItem]





    def to_dict(self) -> dict[str, Any]:
        from ..models.post_public_template_list_response_200_templates_item import PostPublicTemplateListResponse200TemplatesItem
        templates = []
        for templates_item_data in self.templates:
            templates_item = templates_item_data.to_dict()
            templates.append(templates_item)




        field_dict: dict[str, Any] = {}

        field_dict.update({
            "templates": templates,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.post_public_template_list_response_200_templates_item import PostPublicTemplateListResponse200TemplatesItem
        d = dict(src_dict)
        templates = []
        _templates = d.pop("templates")
        for templates_item_data in (_templates):
            templates_item = PostPublicTemplateListResponse200TemplatesItem.from_dict(templates_item_data)



            templates.append(templates_item)


        post_public_template_list_response_200 = cls(
            templates=templates,
        )

        return post_public_template_list_response_200

