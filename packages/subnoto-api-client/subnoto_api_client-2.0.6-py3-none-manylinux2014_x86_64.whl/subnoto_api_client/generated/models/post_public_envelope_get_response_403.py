from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.post_public_envelope_get_response_403_error import PostPublicEnvelopeGetResponse403Error





T = TypeVar("T", bound="PostPublicEnvelopeGetResponse403")



@_attrs_define
class PostPublicEnvelopeGetResponse403:
    """ 
        Attributes:
            status_code (float): HTTP status code
            error (PostPublicEnvelopeGetResponse403Error):
            request_id (str): The unique identifier of the request
            timestamp (str): The timestamp of the response
            path (str): The path of the request
     """

    status_code: float
    error: PostPublicEnvelopeGetResponse403Error
    request_id: str
    timestamp: str
    path: str





    def to_dict(self) -> dict[str, Any]:
        from ..models.post_public_envelope_get_response_403_error import PostPublicEnvelopeGetResponse403Error
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
        from ..models.post_public_envelope_get_response_403_error import PostPublicEnvelopeGetResponse403Error
        d = dict(src_dict)
        status_code = d.pop("statusCode")

        error = PostPublicEnvelopeGetResponse403Error.from_dict(d.pop("error"))




        request_id = d.pop("requestId")

        timestamp = d.pop("timestamp")

        path = d.pop("path")

        post_public_envelope_get_response_403 = cls(
            status_code=status_code,
            error=error,
            request_id=request_id,
            timestamp=timestamp,
            path=path,
        )

        return post_public_envelope_get_response_403

