from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.post_public_envelope_create_response_200_presigned_s3_params_fields import PostPublicEnvelopeCreateResponse200PresignedS3ParamsFields





T = TypeVar("T", bound="PostPublicEnvelopeCreateResponse200PresignedS3Params")



@_attrs_define
class PostPublicEnvelopeCreateResponse200PresignedS3Params:
    """ Pre-signed S3 parameters for document upload. Only returned when no file is provided in the request.

        Attributes:
            url (str): The pre-signed S3 URL for uploading the document.
            fields (PostPublicEnvelopeCreateResponse200PresignedS3ParamsFields): Fields required for the S3 upload.
     """

    url: str
    fields: PostPublicEnvelopeCreateResponse200PresignedS3ParamsFields





    def to_dict(self) -> dict[str, Any]:
        from ..models.post_public_envelope_create_response_200_presigned_s3_params_fields import PostPublicEnvelopeCreateResponse200PresignedS3ParamsFields
        url = self.url

        fields = self.fields.to_dict()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "url": url,
            "fields": fields,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.post_public_envelope_create_response_200_presigned_s3_params_fields import PostPublicEnvelopeCreateResponse200PresignedS3ParamsFields
        d = dict(src_dict)
        url = d.pop("url")

        fields = PostPublicEnvelopeCreateResponse200PresignedS3ParamsFields.from_dict(d.pop("fields"))




        post_public_envelope_create_response_200_presigned_s3_params = cls(
            url=url,
            fields=fields,
        )

        return post_public_envelope_create_response_200_presigned_s3_params

