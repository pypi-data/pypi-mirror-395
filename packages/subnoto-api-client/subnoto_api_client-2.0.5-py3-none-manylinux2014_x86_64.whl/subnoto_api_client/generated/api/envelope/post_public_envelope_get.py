from http import HTTPStatus
from typing import Any, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.post_public_envelope_get_body import PostPublicEnvelopeGetBody
from ...models.post_public_envelope_get_response_200 import PostPublicEnvelopeGetResponse200
from ...models.post_public_envelope_get_response_400 import PostPublicEnvelopeGetResponse400
from ...models.post_public_envelope_get_response_401 import PostPublicEnvelopeGetResponse401
from ...models.post_public_envelope_get_response_403 import PostPublicEnvelopeGetResponse403
from ...models.post_public_envelope_get_response_500 import PostPublicEnvelopeGetResponse500
from typing import cast



def _get_kwargs(
    *,
    body: PostPublicEnvelopeGetBody,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/public/envelope/get",
    }

    _kwargs["json"] = body.to_dict()


    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> PostPublicEnvelopeGetResponse200 | PostPublicEnvelopeGetResponse400 | PostPublicEnvelopeGetResponse401 | PostPublicEnvelopeGetResponse403 | PostPublicEnvelopeGetResponse500 | None:
    if response.status_code == 200:
        response_200 = PostPublicEnvelopeGetResponse200.from_dict(response.json())



        return response_200

    if response.status_code == 400:
        response_400 = PostPublicEnvelopeGetResponse400.from_dict(response.json())



        return response_400

    if response.status_code == 401:
        response_401 = PostPublicEnvelopeGetResponse401.from_dict(response.json())



        return response_401

    if response.status_code == 403:
        response_403 = PostPublicEnvelopeGetResponse403.from_dict(response.json())



        return response_403

    if response.status_code == 500:
        response_500 = PostPublicEnvelopeGetResponse500.from_dict(response.json())



        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[PostPublicEnvelopeGetResponse200 | PostPublicEnvelopeGetResponse400 | PostPublicEnvelopeGetResponse401 | PostPublicEnvelopeGetResponse403 | PostPublicEnvelopeGetResponse500]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: PostPublicEnvelopeGetBody,

) -> Response[PostPublicEnvelopeGetResponse200 | PostPublicEnvelopeGetResponse400 | PostPublicEnvelopeGetResponse401 | PostPublicEnvelopeGetResponse403 | PostPublicEnvelopeGetResponse500]:
    """ get

     Get an envelope by UUID. Returns envelope details, documents, and metrics.

    Args:
        body (PostPublicEnvelopeGetBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PostPublicEnvelopeGetResponse200 | PostPublicEnvelopeGetResponse400 | PostPublicEnvelopeGetResponse401 | PostPublicEnvelopeGetResponse403 | PostPublicEnvelopeGetResponse500]
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
    body: PostPublicEnvelopeGetBody,

) -> PostPublicEnvelopeGetResponse200 | PostPublicEnvelopeGetResponse400 | PostPublicEnvelopeGetResponse401 | PostPublicEnvelopeGetResponse403 | PostPublicEnvelopeGetResponse500 | None:
    """ get

     Get an envelope by UUID. Returns envelope details, documents, and metrics.

    Args:
        body (PostPublicEnvelopeGetBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PostPublicEnvelopeGetResponse200 | PostPublicEnvelopeGetResponse400 | PostPublicEnvelopeGetResponse401 | PostPublicEnvelopeGetResponse403 | PostPublicEnvelopeGetResponse500
     """


    return sync_detailed(
        client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: PostPublicEnvelopeGetBody,

) -> Response[PostPublicEnvelopeGetResponse200 | PostPublicEnvelopeGetResponse400 | PostPublicEnvelopeGetResponse401 | PostPublicEnvelopeGetResponse403 | PostPublicEnvelopeGetResponse500]:
    """ get

     Get an envelope by UUID. Returns envelope details, documents, and metrics.

    Args:
        body (PostPublicEnvelopeGetBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PostPublicEnvelopeGetResponse200 | PostPublicEnvelopeGetResponse400 | PostPublicEnvelopeGetResponse401 | PostPublicEnvelopeGetResponse403 | PostPublicEnvelopeGetResponse500]
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
    body: PostPublicEnvelopeGetBody,

) -> PostPublicEnvelopeGetResponse200 | PostPublicEnvelopeGetResponse400 | PostPublicEnvelopeGetResponse401 | PostPublicEnvelopeGetResponse403 | PostPublicEnvelopeGetResponse500 | None:
    """ get

     Get an envelope by UUID. Returns envelope details, documents, and metrics.

    Args:
        body (PostPublicEnvelopeGetBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PostPublicEnvelopeGetResponse200 | PostPublicEnvelopeGetResponse400 | PostPublicEnvelopeGetResponse401 | PostPublicEnvelopeGetResponse403 | PostPublicEnvelopeGetResponse500
     """


    return (await asyncio_detailed(
        client=client,
body=body,

    )).parsed
