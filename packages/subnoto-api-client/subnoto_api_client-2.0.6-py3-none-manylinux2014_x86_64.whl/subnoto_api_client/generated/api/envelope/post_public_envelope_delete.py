from http import HTTPStatus
from typing import Any, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.post_public_envelope_delete_body import PostPublicEnvelopeDeleteBody
from ...models.post_public_envelope_delete_response_200 import PostPublicEnvelopeDeleteResponse200
from ...models.post_public_envelope_delete_response_400 import PostPublicEnvelopeDeleteResponse400
from ...models.post_public_envelope_delete_response_401 import PostPublicEnvelopeDeleteResponse401
from ...models.post_public_envelope_delete_response_403 import PostPublicEnvelopeDeleteResponse403
from ...models.post_public_envelope_delete_response_500 import PostPublicEnvelopeDeleteResponse500
from typing import cast



def _get_kwargs(
    *,
    body: PostPublicEnvelopeDeleteBody,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/public/envelope/delete",
    }

    _kwargs["json"] = body.to_dict()


    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> PostPublicEnvelopeDeleteResponse200 | PostPublicEnvelopeDeleteResponse400 | PostPublicEnvelopeDeleteResponse401 | PostPublicEnvelopeDeleteResponse403 | PostPublicEnvelopeDeleteResponse500 | None:
    if response.status_code == 200:
        response_200 = PostPublicEnvelopeDeleteResponse200.from_dict(response.json())



        return response_200

    if response.status_code == 400:
        response_400 = PostPublicEnvelopeDeleteResponse400.from_dict(response.json())



        return response_400

    if response.status_code == 401:
        response_401 = PostPublicEnvelopeDeleteResponse401.from_dict(response.json())



        return response_401

    if response.status_code == 403:
        response_403 = PostPublicEnvelopeDeleteResponse403.from_dict(response.json())



        return response_403

    if response.status_code == 500:
        response_500 = PostPublicEnvelopeDeleteResponse500.from_dict(response.json())



        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[PostPublicEnvelopeDeleteResponse200 | PostPublicEnvelopeDeleteResponse400 | PostPublicEnvelopeDeleteResponse401 | PostPublicEnvelopeDeleteResponse403 | PostPublicEnvelopeDeleteResponse500]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: PostPublicEnvelopeDeleteBody,

) -> Response[PostPublicEnvelopeDeleteResponse200 | PostPublicEnvelopeDeleteResponse400 | PostPublicEnvelopeDeleteResponse401 | PostPublicEnvelopeDeleteResponse403 | PostPublicEnvelopeDeleteResponse500]:
    """ delete

     Delete an envelope and all associated data

    Args:
        body (PostPublicEnvelopeDeleteBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PostPublicEnvelopeDeleteResponse200 | PostPublicEnvelopeDeleteResponse400 | PostPublicEnvelopeDeleteResponse401 | PostPublicEnvelopeDeleteResponse403 | PostPublicEnvelopeDeleteResponse500]
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
    body: PostPublicEnvelopeDeleteBody,

) -> PostPublicEnvelopeDeleteResponse200 | PostPublicEnvelopeDeleteResponse400 | PostPublicEnvelopeDeleteResponse401 | PostPublicEnvelopeDeleteResponse403 | PostPublicEnvelopeDeleteResponse500 | None:
    """ delete

     Delete an envelope and all associated data

    Args:
        body (PostPublicEnvelopeDeleteBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PostPublicEnvelopeDeleteResponse200 | PostPublicEnvelopeDeleteResponse400 | PostPublicEnvelopeDeleteResponse401 | PostPublicEnvelopeDeleteResponse403 | PostPublicEnvelopeDeleteResponse500
     """


    return sync_detailed(
        client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: PostPublicEnvelopeDeleteBody,

) -> Response[PostPublicEnvelopeDeleteResponse200 | PostPublicEnvelopeDeleteResponse400 | PostPublicEnvelopeDeleteResponse401 | PostPublicEnvelopeDeleteResponse403 | PostPublicEnvelopeDeleteResponse500]:
    """ delete

     Delete an envelope and all associated data

    Args:
        body (PostPublicEnvelopeDeleteBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PostPublicEnvelopeDeleteResponse200 | PostPublicEnvelopeDeleteResponse400 | PostPublicEnvelopeDeleteResponse401 | PostPublicEnvelopeDeleteResponse403 | PostPublicEnvelopeDeleteResponse500]
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
    body: PostPublicEnvelopeDeleteBody,

) -> PostPublicEnvelopeDeleteResponse200 | PostPublicEnvelopeDeleteResponse400 | PostPublicEnvelopeDeleteResponse401 | PostPublicEnvelopeDeleteResponse403 | PostPublicEnvelopeDeleteResponse500 | None:
    """ delete

     Delete an envelope and all associated data

    Args:
        body (PostPublicEnvelopeDeleteBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PostPublicEnvelopeDeleteResponse200 | PostPublicEnvelopeDeleteResponse400 | PostPublicEnvelopeDeleteResponse401 | PostPublicEnvelopeDeleteResponse403 | PostPublicEnvelopeDeleteResponse500
     """


    return (await asyncio_detailed(
        client=client,
body=body,

    )).parsed
