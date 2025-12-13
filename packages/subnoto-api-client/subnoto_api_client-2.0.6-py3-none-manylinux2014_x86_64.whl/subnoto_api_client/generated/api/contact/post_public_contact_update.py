from http import HTTPStatus
from typing import Any, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.post_public_contact_update_body import PostPublicContactUpdateBody
from ...models.post_public_contact_update_response_200 import PostPublicContactUpdateResponse200
from ...models.post_public_contact_update_response_400 import PostPublicContactUpdateResponse400
from ...models.post_public_contact_update_response_401 import PostPublicContactUpdateResponse401
from ...models.post_public_contact_update_response_403 import PostPublicContactUpdateResponse403
from ...models.post_public_contact_update_response_500 import PostPublicContactUpdateResponse500
from typing import cast



def _get_kwargs(
    *,
    body: PostPublicContactUpdateBody,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/public/contact/update",
    }

    _kwargs["json"] = body.to_dict()


    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> PostPublicContactUpdateResponse200 | PostPublicContactUpdateResponse400 | PostPublicContactUpdateResponse401 | PostPublicContactUpdateResponse403 | PostPublicContactUpdateResponse500 | None:
    if response.status_code == 200:
        response_200 = PostPublicContactUpdateResponse200.from_dict(response.json())



        return response_200

    if response.status_code == 400:
        response_400 = PostPublicContactUpdateResponse400.from_dict(response.json())



        return response_400

    if response.status_code == 401:
        response_401 = PostPublicContactUpdateResponse401.from_dict(response.json())



        return response_401

    if response.status_code == 403:
        response_403 = PostPublicContactUpdateResponse403.from_dict(response.json())



        return response_403

    if response.status_code == 500:
        response_500 = PostPublicContactUpdateResponse500.from_dict(response.json())



        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[PostPublicContactUpdateResponse200 | PostPublicContactUpdateResponse400 | PostPublicContactUpdateResponse401 | PostPublicContactUpdateResponse403 | PostPublicContactUpdateResponse500]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: PostPublicContactUpdateBody,

) -> Response[PostPublicContactUpdateResponse200 | PostPublicContactUpdateResponse400 | PostPublicContactUpdateResponse401 | PostPublicContactUpdateResponse403 | PostPublicContactUpdateResponse500]:
    """ update

     Update a contact inside the workspace.

    Args:
        body (PostPublicContactUpdateBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PostPublicContactUpdateResponse200 | PostPublicContactUpdateResponse400 | PostPublicContactUpdateResponse401 | PostPublicContactUpdateResponse403 | PostPublicContactUpdateResponse500]
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
    body: PostPublicContactUpdateBody,

) -> PostPublicContactUpdateResponse200 | PostPublicContactUpdateResponse400 | PostPublicContactUpdateResponse401 | PostPublicContactUpdateResponse403 | PostPublicContactUpdateResponse500 | None:
    """ update

     Update a contact inside the workspace.

    Args:
        body (PostPublicContactUpdateBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PostPublicContactUpdateResponse200 | PostPublicContactUpdateResponse400 | PostPublicContactUpdateResponse401 | PostPublicContactUpdateResponse403 | PostPublicContactUpdateResponse500
     """


    return sync_detailed(
        client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: PostPublicContactUpdateBody,

) -> Response[PostPublicContactUpdateResponse200 | PostPublicContactUpdateResponse400 | PostPublicContactUpdateResponse401 | PostPublicContactUpdateResponse403 | PostPublicContactUpdateResponse500]:
    """ update

     Update a contact inside the workspace.

    Args:
        body (PostPublicContactUpdateBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PostPublicContactUpdateResponse200 | PostPublicContactUpdateResponse400 | PostPublicContactUpdateResponse401 | PostPublicContactUpdateResponse403 | PostPublicContactUpdateResponse500]
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
    body: PostPublicContactUpdateBody,

) -> PostPublicContactUpdateResponse200 | PostPublicContactUpdateResponse400 | PostPublicContactUpdateResponse401 | PostPublicContactUpdateResponse403 | PostPublicContactUpdateResponse500 | None:
    """ update

     Update a contact inside the workspace.

    Args:
        body (PostPublicContactUpdateBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PostPublicContactUpdateResponse200 | PostPublicContactUpdateResponse400 | PostPublicContactUpdateResponse401 | PostPublicContactUpdateResponse403 | PostPublicContactUpdateResponse500
     """


    return (await asyncio_detailed(
        client=client,
body=body,

    )).parsed
