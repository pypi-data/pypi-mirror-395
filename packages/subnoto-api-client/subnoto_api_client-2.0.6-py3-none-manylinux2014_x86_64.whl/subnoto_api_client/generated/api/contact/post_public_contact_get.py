from http import HTTPStatus
from typing import Any, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.post_public_contact_get_body import PostPublicContactGetBody
from ...models.post_public_contact_get_response_200 import PostPublicContactGetResponse200
from ...models.post_public_contact_get_response_400 import PostPublicContactGetResponse400
from ...models.post_public_contact_get_response_401 import PostPublicContactGetResponse401
from ...models.post_public_contact_get_response_403 import PostPublicContactGetResponse403
from ...models.post_public_contact_get_response_500 import PostPublicContactGetResponse500
from typing import cast



def _get_kwargs(
    *,
    body: PostPublicContactGetBody,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/public/contact/get",
    }

    _kwargs["json"] = body.to_dict()


    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> PostPublicContactGetResponse200 | PostPublicContactGetResponse400 | PostPublicContactGetResponse401 | PostPublicContactGetResponse403 | PostPublicContactGetResponse500 | None:
    if response.status_code == 200:
        response_200 = PostPublicContactGetResponse200.from_dict(response.json())



        return response_200

    if response.status_code == 400:
        response_400 = PostPublicContactGetResponse400.from_dict(response.json())



        return response_400

    if response.status_code == 401:
        response_401 = PostPublicContactGetResponse401.from_dict(response.json())



        return response_401

    if response.status_code == 403:
        response_403 = PostPublicContactGetResponse403.from_dict(response.json())



        return response_403

    if response.status_code == 500:
        response_500 = PostPublicContactGetResponse500.from_dict(response.json())



        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[PostPublicContactGetResponse200 | PostPublicContactGetResponse400 | PostPublicContactGetResponse401 | PostPublicContactGetResponse403 | PostPublicContactGetResponse500]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: PostPublicContactGetBody,

) -> Response[PostPublicContactGetResponse200 | PostPublicContactGetResponse400 | PostPublicContactGetResponse401 | PostPublicContactGetResponse403 | PostPublicContactGetResponse500]:
    """ get

     Get a contact inside the workspace.

    Args:
        body (PostPublicContactGetBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PostPublicContactGetResponse200 | PostPublicContactGetResponse400 | PostPublicContactGetResponse401 | PostPublicContactGetResponse403 | PostPublicContactGetResponse500]
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
    body: PostPublicContactGetBody,

) -> PostPublicContactGetResponse200 | PostPublicContactGetResponse400 | PostPublicContactGetResponse401 | PostPublicContactGetResponse403 | PostPublicContactGetResponse500 | None:
    """ get

     Get a contact inside the workspace.

    Args:
        body (PostPublicContactGetBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PostPublicContactGetResponse200 | PostPublicContactGetResponse400 | PostPublicContactGetResponse401 | PostPublicContactGetResponse403 | PostPublicContactGetResponse500
     """


    return sync_detailed(
        client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: PostPublicContactGetBody,

) -> Response[PostPublicContactGetResponse200 | PostPublicContactGetResponse400 | PostPublicContactGetResponse401 | PostPublicContactGetResponse403 | PostPublicContactGetResponse500]:
    """ get

     Get a contact inside the workspace.

    Args:
        body (PostPublicContactGetBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PostPublicContactGetResponse200 | PostPublicContactGetResponse400 | PostPublicContactGetResponse401 | PostPublicContactGetResponse403 | PostPublicContactGetResponse500]
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
    body: PostPublicContactGetBody,

) -> PostPublicContactGetResponse200 | PostPublicContactGetResponse400 | PostPublicContactGetResponse401 | PostPublicContactGetResponse403 | PostPublicContactGetResponse500 | None:
    """ get

     Get a contact inside the workspace.

    Args:
        body (PostPublicContactGetBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PostPublicContactGetResponse200 | PostPublicContactGetResponse400 | PostPublicContactGetResponse401 | PostPublicContactGetResponse403 | PostPublicContactGetResponse500
     """


    return (await asyncio_detailed(
        client=client,
body=body,

    )).parsed
