from http import HTTPStatus
from typing import Any, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.post_public_contact_create_body import PostPublicContactCreateBody
from ...models.post_public_contact_create_response_200 import PostPublicContactCreateResponse200
from ...models.post_public_contact_create_response_400 import PostPublicContactCreateResponse400
from ...models.post_public_contact_create_response_401 import PostPublicContactCreateResponse401
from ...models.post_public_contact_create_response_403 import PostPublicContactCreateResponse403
from ...models.post_public_contact_create_response_500 import PostPublicContactCreateResponse500
from typing import cast



def _get_kwargs(
    *,
    body: PostPublicContactCreateBody,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/public/contact/create",
    }

    _kwargs["json"] = body.to_dict()


    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> PostPublicContactCreateResponse200 | PostPublicContactCreateResponse400 | PostPublicContactCreateResponse401 | PostPublicContactCreateResponse403 | PostPublicContactCreateResponse500 | None:
    if response.status_code == 200:
        response_200 = PostPublicContactCreateResponse200.from_dict(response.json())



        return response_200

    if response.status_code == 400:
        response_400 = PostPublicContactCreateResponse400.from_dict(response.json())



        return response_400

    if response.status_code == 401:
        response_401 = PostPublicContactCreateResponse401.from_dict(response.json())



        return response_401

    if response.status_code == 403:
        response_403 = PostPublicContactCreateResponse403.from_dict(response.json())



        return response_403

    if response.status_code == 500:
        response_500 = PostPublicContactCreateResponse500.from_dict(response.json())



        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[PostPublicContactCreateResponse200 | PostPublicContactCreateResponse400 | PostPublicContactCreateResponse401 | PostPublicContactCreateResponse403 | PostPublicContactCreateResponse500]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: PostPublicContactCreateBody,

) -> Response[PostPublicContactCreateResponse200 | PostPublicContactCreateResponse400 | PostPublicContactCreateResponse401 | PostPublicContactCreateResponse403 | PostPublicContactCreateResponse500]:
    """ create

     Create a contact inside the workspace.

    Args:
        body (PostPublicContactCreateBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PostPublicContactCreateResponse200 | PostPublicContactCreateResponse400 | PostPublicContactCreateResponse401 | PostPublicContactCreateResponse403 | PostPublicContactCreateResponse500]
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
    body: PostPublicContactCreateBody,

) -> PostPublicContactCreateResponse200 | PostPublicContactCreateResponse400 | PostPublicContactCreateResponse401 | PostPublicContactCreateResponse403 | PostPublicContactCreateResponse500 | None:
    """ create

     Create a contact inside the workspace.

    Args:
        body (PostPublicContactCreateBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PostPublicContactCreateResponse200 | PostPublicContactCreateResponse400 | PostPublicContactCreateResponse401 | PostPublicContactCreateResponse403 | PostPublicContactCreateResponse500
     """


    return sync_detailed(
        client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: PostPublicContactCreateBody,

) -> Response[PostPublicContactCreateResponse200 | PostPublicContactCreateResponse400 | PostPublicContactCreateResponse401 | PostPublicContactCreateResponse403 | PostPublicContactCreateResponse500]:
    """ create

     Create a contact inside the workspace.

    Args:
        body (PostPublicContactCreateBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PostPublicContactCreateResponse200 | PostPublicContactCreateResponse400 | PostPublicContactCreateResponse401 | PostPublicContactCreateResponse403 | PostPublicContactCreateResponse500]
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
    body: PostPublicContactCreateBody,

) -> PostPublicContactCreateResponse200 | PostPublicContactCreateResponse400 | PostPublicContactCreateResponse401 | PostPublicContactCreateResponse403 | PostPublicContactCreateResponse500 | None:
    """ create

     Create a contact inside the workspace.

    Args:
        body (PostPublicContactCreateBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PostPublicContactCreateResponse200 | PostPublicContactCreateResponse400 | PostPublicContactCreateResponse401 | PostPublicContactCreateResponse403 | PostPublicContactCreateResponse500
     """


    return (await asyncio_detailed(
        client=client,
body=body,

    )).parsed
