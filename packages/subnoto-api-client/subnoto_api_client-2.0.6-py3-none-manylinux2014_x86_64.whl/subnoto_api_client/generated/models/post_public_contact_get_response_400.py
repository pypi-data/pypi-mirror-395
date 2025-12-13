from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.post_public_contact_get_response_400_error import PostPublicContactGetResponse400Error





T = TypeVar("T", bound="PostPublicContactGetResponse400")



@_attrs_define
class PostPublicContactGetResponse400:
    """ 
        Attributes:
            status_code (float): HTTP status code
            error (PostPublicContactGetResponse400Error):
            request_id (str): The unique identifier of the request
            timestamp (str): The timestamp of the response
            path (str): The path of the request
     """

    status_code: float
    error: PostPublicContactGetResponse400Error
    request_id: str
    timestamp: str
    path: str





    def to_dict(self) -> dict[str, Any]:
        from ..models.post_public_contact_get_response_400_error import PostPublicContactGetResponse400Error
        status_code = self.status_code

        error = self.error.to_dict()

        request_id = self.request_id

        timestamp = self.timestamp

        path = self.path


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "statusCode": status_code,
            "error": error,
            "requestId": request_id,
            "timestamp": timestamp,
            "path": path,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.post_public_contact_get_response_400_error import PostPublicContactGetResponse400Error
        d = dict(src_dict)
        status_code = d.pop("statusCode")

        error = PostPublicContactGetResponse400Error.from_dict(d.pop("error"))




        request_id = d.pop("requestId")

        timestamp = d.pop("timestamp")

        path = d.pop("path")

        post_public_contact_get_response_400 = cls(
            status_code=status_code,
            error=error,
            request_id=request_id,
            timestamp=timestamp,
            path=path,
        )

        return post_public_contact_get_response_400

