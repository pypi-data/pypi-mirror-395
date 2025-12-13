from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.post_public_envelope_create_response_200_presigned_s3_params import PostPublicEnvelopeCreateResponse200PresignedS3Params





T = TypeVar("T", bound="PostPublicEnvelopeCreateResponse200")



@_attrs_define
class PostPublicEnvelopeCreateResponse200:
    """ 
        Attributes:
            envelope_uuid (str): The unique identifier of the created envelope.
            document_uuid (str): The unique identifier of the first document.
            revision_encryption_key (str): The encryption key in base64 for the document revision to be used for encryption.
            presigned_s3_params (PostPublicEnvelopeCreateResponse200PresignedS3Params | Unset): Pre-signed S3 parameters for
                document upload. Only returned when no file is provided in the request.
     """

    envelope_uuid: str
    document_uuid: str
    revision_encryption_key: str
    presigned_s3_params: PostPublicEnvelopeCreateResponse200PresignedS3Params | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.post_public_envelope_create_response_200_presigned_s3_params import PostPublicEnvelopeCreateResponse200PresignedS3Params
        envelope_uuid = self.envelope_uuid

        document_uuid = self.document_uuid

        revision_encryption_key = self.revision_encryption_key

        presigned_s3_params: dict[str, Any] | Unset = UNSET
        if not isinstance(self.presigned_s3_params, Unset):
            presigned_s3_params = self.presigned_s3_params.to_dict()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "envelopeUuid": envelope_uuid,
            "documentUuid": document_uuid,
            "revisionEncryptionKey": revision_encryption_key,
        })
        if presigned_s3_params is not UNSET:
            field_dict["presignedS3Params"] = presigned_s3_params

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.post_public_envelope_create_response_200_presigned_s3_params import PostPublicEnvelopeCreateResponse200PresignedS3Params
        d = dict(src_dict)
        envelope_uuid = d.pop("envelopeUuid")

        document_uuid = d.pop("documentUuid")

        revision_encryption_key = d.pop("revisionEncryptionKey")

        _presigned_s3_params = d.pop("presignedS3Params", UNSET)
        presigned_s3_params: PostPublicEnvelopeCreateResponse200PresignedS3Params | Unset
        if isinstance(_presigned_s3_params,  Unset):
            presigned_s3_params = UNSET
        else:
            presigned_s3_params = PostPublicEnvelopeCreateResponse200PresignedS3Params.from_dict(_presigned_s3_params)




        post_public_envelope_create_response_200 = cls(
            envelope_uuid=envelope_uuid,
            document_uuid=document_uuid,
            revision_encryption_key=revision_encryption_key,
            presigned_s3_params=presigned_s3_params,
        )

        return post_public_envelope_create_response_200

