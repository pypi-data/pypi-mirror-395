from http import HTTPStatus
from typing import Any, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.post_public_contact_delete_body import PostPublicContactDeleteBody
from ...models.post_public_contact_delete_response_200 import PostPublicContactDeleteResponse200
from ...models.post_public_contact_delete_response_400 import PostPublicContactDeleteResponse400
from ...models.post_public_contact_delete_response_401 import PostPublicContactDeleteResponse401
from ...models.post_public_contact_delete_response_403 import PostPublicContactDeleteResponse403
from ...models.post_public_contact_delete_response_500 import PostPublicContactDeleteResponse500
from typing import cast



def _get_kwargs(
    *,
    body: PostPublicContactDeleteBody,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/public/contact/delete",
    }

    _kwargs["json"] = body.to_dict()


    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> PostPublicContactDeleteResponse200 | PostPublicContactDeleteResponse400 | PostPublicContactDeleteResponse401 | PostPublicContactDeleteResponse403 | PostPublicContactDeleteResponse500 | None:
    if response.status_code == 200:
        response_200 = PostPublicContactDeleteResponse200.from_dict(response.json())



        return response_200

    if response.status_code == 400:
        response_400 = PostPublicContactDeleteResponse400.from_dict(response.json())



        return response_400

    if response.status_code == 401:
        response_401 = PostPublicContactDeleteResponse401.from_dict(response.json())



        return response_401

    if response.status_code == 403:
        response_403 = PostPublicContactDeleteResponse403.from_dict(response.json())



        return response_403

    if response.status_code == 500:
        response_500 = PostPublicContactDeleteResponse500.from_dict(response.json())



        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[PostPublicContactDeleteResponse200 | PostPublicContactDeleteResponse400 | PostPublicContactDeleteResponse401 | PostPublicContactDeleteResponse403 | PostPublicContactDeleteResponse500]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: PostPublicContactDeleteBody,

) -> Response[PostPublicContactDeleteResponse200 | PostPublicContactDeleteResponse400 | PostPublicContactDeleteResponse401 | PostPublicContactDeleteResponse403 | PostPublicContactDeleteResponse500]:
    """ delete

     Delete a contact inside the workspace.

    Args:
        body (PostPublicContactDeleteBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PostPublicContactDeleteResponse200 | PostPublicContactDeleteResponse400 | PostPublicContactDeleteResponse401 | PostPublicContactDeleteResponse403 | PostPublicContactDeleteResponse500]
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
    body: PostPublicContactDeleteBody,

) -> PostPublicContactDeleteResponse200 | PostPublicContactDeleteResponse400 | PostPublicContactDeleteResponse401 | PostPublicContactDeleteResponse403 | PostPublicContactDeleteResponse500 | None:
    """ delete

     Delete a contact inside the workspace.

    Args:
        body (PostPublicContactDeleteBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PostPublicContactDeleteResponse200 | PostPublicContactDeleteResponse400 | PostPublicContactDeleteResponse401 | PostPublicContactDeleteResponse403 | PostPublicContactDeleteResponse500
     """


    return sync_detailed(
        client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: PostPublicContactDeleteBody,

) -> Response[PostPublicContactDeleteResponse200 | PostPublicContactDeleteResponse400 | PostPublicContactDeleteResponse401 | PostPublicContactDeleteResponse403 | PostPublicContactDeleteResponse500]:
    """ delete

     Delete a contact inside the workspace.

    Args:
        body (PostPublicContactDeleteBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PostPublicContactDeleteResponse200 | PostPublicContactDeleteResponse400 | PostPublicContactDeleteResponse401 | PostPublicContactDeleteResponse403 | PostPublicContactDeleteResponse500]
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
    body: PostPublicContactDeleteBody,

) -> PostPublicContactDeleteResponse200 | PostPublicContactDeleteResponse400 | PostPublicContactDeleteResponse401 | PostPublicContactDeleteResponse403 | PostPublicContactDeleteResponse500 | None:
    """ delete

     Delete a contact inside the workspace.

    Args:
        body (PostPublicContactDeleteBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PostPublicContactDeleteResponse200 | PostPublicContactDeleteResponse400 | PostPublicContactDeleteResponse401 | PostPublicContactDeleteResponse403 | PostPublicContactDeleteResponse500
     """


    return (await asyncio_detailed(
        client=client,
body=body,

    )).parsed
