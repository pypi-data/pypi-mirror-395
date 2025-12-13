from http import HTTPStatus
from typing import Any, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.post_public_contact_list_body import PostPublicContactListBody
from ...models.post_public_contact_list_response_200 import PostPublicContactListResponse200
from ...models.post_public_contact_list_response_400 import PostPublicContactListResponse400
from ...models.post_public_contact_list_response_401 import PostPublicContactListResponse401
from ...models.post_public_contact_list_response_403 import PostPublicContactListResponse403
from ...models.post_public_contact_list_response_500 import PostPublicContactListResponse500
from typing import cast



def _get_kwargs(
    *,
    body: PostPublicContactListBody,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/public/contact/list",
    }

    _kwargs["json"] = body.to_dict()


    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> PostPublicContactListResponse200 | PostPublicContactListResponse400 | PostPublicContactListResponse401 | PostPublicContactListResponse403 | PostPublicContactListResponse500 | None:
    if response.status_code == 200:
        response_200 = PostPublicContactListResponse200.from_dict(response.json())



        return response_200

    if response.status_code == 400:
        response_400 = PostPublicContactListResponse400.from_dict(response.json())



        return response_400

    if response.status_code == 401:
        response_401 = PostPublicContactListResponse401.from_dict(response.json())



        return response_401

    if response.status_code == 403:
        response_403 = PostPublicContactListResponse403.from_dict(response.json())



        return response_403

    if response.status_code == 500:
        response_500 = PostPublicContactListResponse500.from_dict(response.json())



        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[PostPublicContactListResponse200 | PostPublicContactListResponse400 | PostPublicContactListResponse401 | PostPublicContactListResponse403 | PostPublicContactListResponse500]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: PostPublicContactListBody,

) -> Response[PostPublicContactListResponse200 | PostPublicContactListResponse400 | PostPublicContactListResponse401 | PostPublicContactListResponse403 | PostPublicContactListResponse500]:
    """ list

     List all contacts inside the workspace.

    Args:
        body (PostPublicContactListBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PostPublicContactListResponse200 | PostPublicContactListResponse400 | PostPublicContactListResponse401 | PostPublicContactListResponse403 | PostPublicContactListResponse500]
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
    body: PostPublicContactListBody,

) -> PostPublicContactListResponse200 | PostPublicContactListResponse400 | PostPublicContactListResponse401 | PostPublicContactListResponse403 | PostPublicContactListResponse500 | None:
    """ list

     List all contacts inside the workspace.

    Args:
        body (PostPublicContactListBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PostPublicContactListResponse200 | PostPublicContactListResponse400 | PostPublicContactListResponse401 | PostPublicContactListResponse403 | PostPublicContactListResponse500
     """


    return sync_detailed(
        client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: PostPublicContactListBody,

) -> Response[PostPublicContactListResponse200 | PostPublicContactListResponse400 | PostPublicContactListResponse401 | PostPublicContactListResponse403 | PostPublicContactListResponse500]:
    """ list

     List all contacts inside the workspace.

    Args:
        body (PostPublicContactListBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PostPublicContactListResponse200 | PostPublicContactListResponse400 | PostPublicContactListResponse401 | PostPublicContactListResponse403 | PostPublicContactListResponse500]
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
    body: PostPublicContactListBody,

) -> PostPublicContactListResponse200 | PostPublicContactListResponse400 | PostPublicContactListResponse401 | PostPublicContactListResponse403 | PostPublicContactListResponse500 | None:
    """ list

     List all contacts inside the workspace.

    Args:
        body (PostPublicContactListBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PostPublicContactListResponse200 | PostPublicContactListResponse400 | PostPublicContactListResponse401 | PostPublicContactListResponse403 | PostPublicContactListResponse500
     """


    return (await asyncio_detailed(
        client=client,
body=body,

    )).parsed
