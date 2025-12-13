from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.post_public_envelope_update_response_401_error_code import PostPublicEnvelopeUpdateResponse401ErrorCode






T = TypeVar("T", bound="PostPublicEnvelopeUpdateResponse401Error")



@_attrs_define
class PostPublicEnvelopeUpdateResponse401Error:
    """ 
        Attributes:
            code (PostPublicEnvelopeUpdateResponse401ErrorCode): The error code
            message (str): The error message
            suggestion (str): A suggestion to resolve the error
            documentation_url (str): A URL to the documentation
     """

    code: PostPublicEnvelopeUpdateResponse401ErrorCode
    message: str
    suggestion: str
    documentation_url: str





    def to_dict(self) -> dict[str, Any]:
        code = self.code.value

        message = self.message

        suggestion = self.suggestion

        documentation_url = self.documentation_url


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "code": code,
            "message": message,
            "suggestion": suggestion,
            "documentationUrl": documentation_url,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        code = PostPublicEnvelopeUpdateResponse401ErrorCode(d.pop("code"))




        message = d.pop("message")

        suggestion = d.pop("suggestion")

        documentation_url = d.pop("documentationUrl")

        post_public_envelope_update_response_401_error = cls(
            code=code,
            message=message,
            suggestion=suggestion,
            documentation_url=documentation_url,
        )

        return post_public_envelope_update_response_401_error

