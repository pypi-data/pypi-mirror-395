from http import HTTPStatus
from typing import Any, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.post_public_envelope_add_blocks_body import PostPublicEnvelopeAddBlocksBody
from ...models.post_public_envelope_add_blocks_response_200 import PostPublicEnvelopeAddBlocksResponse200
from ...models.post_public_envelope_add_blocks_response_400 import PostPublicEnvelopeAddBlocksResponse400
from ...models.post_public_envelope_add_blocks_response_401 import PostPublicEnvelopeAddBlocksResponse401
from ...models.post_public_envelope_add_blocks_response_403 import PostPublicEnvelopeAddBlocksResponse403
from ...models.post_public_envelope_add_blocks_response_500 import PostPublicEnvelopeAddBlocksResponse500
from typing import cast



def _get_kwargs(
    *,
    body: PostPublicEnvelopeAddBlocksBody,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/public/envelope/add-blocks",
    }

    _kwargs["json"] = body.to_dict()


    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> PostPublicEnvelopeAddBlocksResponse200 | PostPublicEnvelopeAddBlocksResponse400 | PostPublicEnvelopeAddBlocksResponse401 | PostPublicEnvelopeAddBlocksResponse403 | PostPublicEnvelopeAddBlocksResponse500 | None:
    if response.status_code == 200:
        response_200 = PostPublicEnvelopeAddBlocksResponse200.from_dict(response.json())



        return response_200

    if response.status_code == 400:
        response_400 = PostPublicEnvelopeAddBlocksResponse400.from_dict(response.json())



        return response_400

    if response.status_code == 401:
        response_401 = PostPublicEnvelopeAddBlocksResponse401.from_dict(response.json())



        return response_401

    if response.status_code == 403:
        response_403 = PostPublicEnvelopeAddBlocksResponse403.from_dict(response.json())



        return response_403

    if response.status_code == 500:
        response_500 = PostPublicEnvelopeAddBlocksResponse500.from_dict(response.json())



        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[PostPublicEnvelopeAddBlocksResponse200 | PostPublicEnvelopeAddBlocksResponse400 | PostPublicEnvelopeAddBlocksResponse401 | PostPublicEnvelopeAddBlocksResponse403 | PostPublicEnvelopeAddBlocksResponse500]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: PostPublicEnvelopeAddBlocksBody,

) -> Response[PostPublicEnvelopeAddBlocksResponse200 | PostPublicEnvelopeAddBlocksResponse400 | PostPublicEnvelopeAddBlocksResponse401 | PostPublicEnvelopeAddBlocksResponse403 | PostPublicEnvelopeAddBlocksResponse500]:
    """ add-blocks

     Add blocks to a document snapshot in an envelope

    Args:
        body (PostPublicEnvelopeAddBlocksBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PostPublicEnvelopeAddBlocksResponse200 | PostPublicEnvelopeAddBlocksResponse400 | PostPublicEnvelopeAddBlocksResponse401 | PostPublicEnvelopeAddBlocksResponse403 | PostPublicEnvelopeAddBlocksResponse500]
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
    body: PostPublicEnvelopeAddBlocksBody,

) -> PostPublicEnvelopeAddBlocksResponse200 | PostPublicEnvelopeAddBlocksResponse400 | PostPublicEnvelopeAddBlocksResponse401 | PostPublicEnvelopeAddBlocksResponse403 | PostPublicEnvelopeAddBlocksResponse500 | None:
    """ add-blocks

     Add blocks to a document snapshot in an envelope

    Args:
        body (PostPublicEnvelopeAddBlocksBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PostPublicEnvelopeAddBlocksResponse200 | PostPublicEnvelopeAddBlocksResponse400 | PostPublicEnvelopeAddBlocksResponse401 | PostPublicEnvelopeAddBlocksResponse403 | PostPublicEnvelopeAddBlocksResponse500
     """


    return sync_detailed(
        client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: PostPublicEnvelopeAddBlocksBody,

) -> Response[PostPublicEnvelopeAddBlocksResponse200 | PostPublicEnvelopeAddBlocksResponse400 | PostPublicEnvelopeAddBlocksResponse401 | PostPublicEnvelopeAddBlocksResponse403 | PostPublicEnvelopeAddBlocksResponse500]:
    """ add-blocks

     Add blocks to a document snapshot in an envelope

    Args:
        body (PostPublicEnvelopeAddBlocksBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PostPublicEnvelopeAddBlocksResponse200 | PostPublicEnvelopeAddBlocksResponse400 | PostPublicEnvelopeAddBlocksResponse401 | PostPublicEnvelopeAddBlocksResponse403 | PostPublicEnvelopeAddBlocksResponse500]
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
    body: PostPublicEnvelopeAddBlocksBody,

) -> PostPublicEnvelopeAddBlocksResponse200 | PostPublicEnvelopeAddBlocksResponse400 | PostPublicEnvelopeAddBlocksResponse401 | PostPublicEnvelopeAddBlocksResponse403 | PostPublicEnvelopeAddBlocksResponse500 | None:
    """ add-blocks

     Add blocks to a document snapshot in an envelope

    Args:
        body (PostPublicEnvelopeAddBlocksBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PostPublicEnvelopeAddBlocksResponse200 | PostPublicEnvelopeAddBlocksResponse400 | PostPublicEnvelopeAddBlocksResponse401 | PostPublicEnvelopeAddBlocksResponse403 | PostPublicEnvelopeAddBlocksResponse500
     """


    return (await asyncio_detailed(
        client=client,
body=body,

    )).parsed
