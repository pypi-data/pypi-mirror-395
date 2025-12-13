from http import HTTPStatus
from typing import Any, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.post_public_envelope_create_body import PostPublicEnvelopeCreateBody
from ...models.post_public_envelope_create_response_200 import PostPublicEnvelopeCreateResponse200
from ...models.post_public_envelope_create_response_400 import PostPublicEnvelopeCreateResponse400
from ...models.post_public_envelope_create_response_401 import PostPublicEnvelopeCreateResponse401
from ...models.post_public_envelope_create_response_403 import PostPublicEnvelopeCreateResponse403
from ...models.post_public_envelope_create_response_500 import PostPublicEnvelopeCreateResponse500
from typing import cast



def _get_kwargs(
    *,
    body: PostPublicEnvelopeCreateBody,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/public/envelope/create",
    }

    _kwargs["json"] = body.to_dict()


    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> PostPublicEnvelopeCreateResponse200 | PostPublicEnvelopeCreateResponse400 | PostPublicEnvelopeCreateResponse401 | PostPublicEnvelopeCreateResponse403 | PostPublicEnvelopeCreateResponse500 | None:
    if response.status_code == 200:
        response_200 = PostPublicEnvelopeCreateResponse200.from_dict(response.json())



        return response_200

    if response.status_code == 400:
        response_400 = PostPublicEnvelopeCreateResponse400.from_dict(response.json())



        return response_400

    if response.status_code == 401:
        response_401 = PostPublicEnvelopeCreateResponse401.from_dict(response.json())



        return response_401

    if response.status_code == 403:
        response_403 = PostPublicEnvelopeCreateResponse403.from_dict(response.json())



        return response_403

    if response.status_code == 500:
        response_500 = PostPublicEnvelopeCreateResponse500.from_dict(response.json())



        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[PostPublicEnvelopeCreateResponse200 | PostPublicEnvelopeCreateResponse400 | PostPublicEnvelopeCreateResponse401 | PostPublicEnvelopeCreateResponse403 | PostPublicEnvelopeCreateResponse500]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: PostPublicEnvelopeCreateBody,

) -> Response[PostPublicEnvelopeCreateResponse200 | PostPublicEnvelopeCreateResponse400 | PostPublicEnvelopeCreateResponse401 | PostPublicEnvelopeCreateResponse403 | PostPublicEnvelopeCreateResponse500]:
    """ create

     Create an envelope and the first document placeholder. Optionally accepts a small file directly (max
    10 MB) in the request body. If a file is provided, it will be encrypted and uploaded to S3, and pre-
    signed S3 parameters will not be returned. Otherwise, returns pre-signed S3 parameters for document
    upload.

    Args:
        body (PostPublicEnvelopeCreateBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PostPublicEnvelopeCreateResponse200 | PostPublicEnvelopeCreateResponse400 | PostPublicEnvelopeCreateResponse401 | PostPublicEnvelopeCreateResponse403 | PostPublicEnvelopeCreateResponse500]
     """


    kwargs = _get_kwargs(
        body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: AuthenticatedClient | Client,
    body: PostPublicEnvelopeCreateBody,

) -> PostPublicEnvelopeCreateResponse200 | PostPublicEnvelopeCreateResponse400 | PostPublicEnvelopeCreateResponse401 | PostPublicEnvelopeCreateResponse403 | PostPublicEnvelopeCreateResponse500 | None:
    """ create

     Create an envelope and the first document placeholder. Optionally accepts a small file directly (max
    10 MB) in the request body. If a file is provided, it will be encrypted and uploaded to S3, and pre-
    signed S3 parameters will not be returned. Otherwise, returns pre-signed S3 parameters for document
    upload.

    Args:
        body (PostPublicEnvelopeCreateBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PostPublicEnvelopeCreateResponse200 | PostPublicEnvelopeCreateResponse400 | PostPublicEnvelopeCreateResponse401 | PostPublicEnvelopeCreateResponse403 | PostPublicEnvelopeCreateResponse500
     """


    return sync_detailed(
        client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: PostPublicEnvelopeCreateBody,

) -> Response[PostPublicEnvelopeCreateResponse200 | PostPublicEnvelopeCreateResponse400 | PostPublicEnvelopeCreateResponse401 | PostPublicEnvelopeCreateResponse403 | PostPublicEnvelopeCreateResponse500]:
    """ create

     Create an envelope and the first document placeholder. Optionally accepts a small file directly (max
    10 MB) in the request body. If a file is provided, it will be encrypted and uploaded to S3, and pre-
    signed S3 parameters will not be returned. Otherwise, returns pre-signed S3 parameters for document
    upload.

    Args:
        body (PostPublicEnvelopeCreateBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PostPublicEnvelopeCreateResponse200 | PostPublicEnvelopeCreateResponse400 | PostPublicEnvelopeCreateResponse401 | PostPublicEnvelopeCreateResponse403 | PostPublicEnvelopeCreateResponse500]
     """


    kwargs = _get_kwargs(
        body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: PostPublicEnvelopeCreateBody,

) -> PostPublicEnvelopeCreateResponse200 | PostPublicEnvelopeCreateResponse400 | PostPublicEnvelopeCreateResponse401 | PostPublicEnvelopeCreateResponse403 | PostPublicEnvelopeCreateResponse500 | None:
    """ create

     Create an envelope and the first document placeholder. Optionally accepts a small file directly (max
    10 MB) in the request body. If a file is provided, it will be encrypted and uploaded to S3, and pre-
    signed S3 parameters will not be returned. Otherwise, returns pre-signed S3 parameters for document
    upload.

    Args:
        body (PostPublicEnvelopeCreateBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PostPublicEnvelopeCreateResponse200 | PostPublicEnvelopeCreateResponse400 | PostPublicEnvelopeCreateResponse401 | PostPublicEnvelopeCreateResponse403 | PostPublicEnvelopeCreateResponse500
     """


    return (await asyncio_detailed(
        client=client,
body=body,

    )).parsed
