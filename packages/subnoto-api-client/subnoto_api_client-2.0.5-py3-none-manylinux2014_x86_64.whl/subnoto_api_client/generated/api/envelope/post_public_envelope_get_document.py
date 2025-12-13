from http import HTTPStatus
from typing import Any, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.post_public_envelope_get_document_body import PostPublicEnvelopeGetDocumentBody
from ...models.post_public_envelope_get_document_response_400 import PostPublicEnvelopeGetDocumentResponse400
from ...models.post_public_envelope_get_document_response_401 import PostPublicEnvelopeGetDocumentResponse401
from ...models.post_public_envelope_get_document_response_403 import PostPublicEnvelopeGetDocumentResponse403
from ...models.post_public_envelope_get_document_response_500 import PostPublicEnvelopeGetDocumentResponse500
from typing import cast



def _get_kwargs(
    *,
    body: PostPublicEnvelopeGetDocumentBody,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/public/envelope/get-document",
    }

    _kwargs["json"] = body.to_dict()


    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Any | PostPublicEnvelopeGetDocumentResponse400 | PostPublicEnvelopeGetDocumentResponse401 | PostPublicEnvelopeGetDocumentResponse403 | PostPublicEnvelopeGetDocumentResponse500 | None:
    if response.status_code == 200:
        response_200 = cast(Any, response.content)
        return response_200

    if response.status_code == 400:
        response_400 = PostPublicEnvelopeGetDocumentResponse400.from_dict(response.content)



        return response_400

    if response.status_code == 401:
        response_401 = PostPublicEnvelopeGetDocumentResponse401.from_dict(response.content)



        return response_401

    if response.status_code == 403:
        response_403 = PostPublicEnvelopeGetDocumentResponse403.from_dict(response.content)



        return response_403

    if response.status_code == 500:
        response_500 = PostPublicEnvelopeGetDocumentResponse500.from_dict(response.content)



        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Any | PostPublicEnvelopeGetDocumentResponse400 | PostPublicEnvelopeGetDocumentResponse401 | PostPublicEnvelopeGetDocumentResponse403 | PostPublicEnvelopeGetDocumentResponse500]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: PostPublicEnvelopeGetDocumentBody,

) -> Response[Any | PostPublicEnvelopeGetDocumentResponse400 | PostPublicEnvelopeGetDocumentResponse401 | PostPublicEnvelopeGetDocumentResponse403 | PostPublicEnvelopeGetDocumentResponse500]:
    """ get-document

     Download the latest version of a document from an envelope.

    Args:
        body (PostPublicEnvelopeGetDocumentBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | PostPublicEnvelopeGetDocumentResponse400 | PostPublicEnvelopeGetDocumentResponse401 | PostPublicEnvelopeGetDocumentResponse403 | PostPublicEnvelopeGetDocumentResponse500]
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
    body: PostPublicEnvelopeGetDocumentBody,

) -> Any | PostPublicEnvelopeGetDocumentResponse400 | PostPublicEnvelopeGetDocumentResponse401 | PostPublicEnvelopeGetDocumentResponse403 | PostPublicEnvelopeGetDocumentResponse500 | None:
    """ get-document

     Download the latest version of a document from an envelope.

    Args:
        body (PostPublicEnvelopeGetDocumentBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | PostPublicEnvelopeGetDocumentResponse400 | PostPublicEnvelopeGetDocumentResponse401 | PostPublicEnvelopeGetDocumentResponse403 | PostPublicEnvelopeGetDocumentResponse500
     """


    return sync_detailed(
        client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: PostPublicEnvelopeGetDocumentBody,

) -> Response[Any | PostPublicEnvelopeGetDocumentResponse400 | PostPublicEnvelopeGetDocumentResponse401 | PostPublicEnvelopeGetDocumentResponse403 | PostPublicEnvelopeGetDocumentResponse500]:
    """ get-document

     Download the latest version of a document from an envelope.

    Args:
        body (PostPublicEnvelopeGetDocumentBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | PostPublicEnvelopeGetDocumentResponse400 | PostPublicEnvelopeGetDocumentResponse401 | PostPublicEnvelopeGetDocumentResponse403 | PostPublicEnvelopeGetDocumentResponse500]
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
    body: PostPublicEnvelopeGetDocumentBody,

) -> Any | PostPublicEnvelopeGetDocumentResponse400 | PostPublicEnvelopeGetDocumentResponse401 | PostPublicEnvelopeGetDocumentResponse403 | PostPublicEnvelopeGetDocumentResponse500 | None:
    """ get-document

     Download the latest version of a document from an envelope.

    Args:
        body (PostPublicEnvelopeGetDocumentBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | PostPublicEnvelopeGetDocumentResponse400 | PostPublicEnvelopeGetDocumentResponse401 | PostPublicEnvelopeGetDocumentResponse403 | PostPublicEnvelopeGetDocumentResponse500
     """


    return (await asyncio_detailed(
        client=client,
body=body,

    )).parsed
