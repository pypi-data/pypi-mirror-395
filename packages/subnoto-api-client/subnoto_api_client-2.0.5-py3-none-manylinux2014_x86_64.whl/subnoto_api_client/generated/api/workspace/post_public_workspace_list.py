from http import HTTPStatus
from typing import Any, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.post_public_workspace_list_body import PostPublicWorkspaceListBody
from ...models.post_public_workspace_list_response_200 import PostPublicWorkspaceListResponse200
from ...models.post_public_workspace_list_response_401 import PostPublicWorkspaceListResponse401
from ...models.post_public_workspace_list_response_403 import PostPublicWorkspaceListResponse403
from ...models.post_public_workspace_list_response_500 import PostPublicWorkspaceListResponse500
from typing import cast



def _get_kwargs(
    *,
    body: PostPublicWorkspaceListBody,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/public/workspace/list",
    }

    _kwargs["json"] = body.to_dict()


    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> PostPublicWorkspaceListResponse200 | PostPublicWorkspaceListResponse401 | PostPublicWorkspaceListResponse403 | PostPublicWorkspaceListResponse500 | None:
    if response.status_code == 200:
        response_200 = PostPublicWorkspaceListResponse200.from_dict(response.json())



        return response_200

    if response.status_code == 401:
        response_401 = PostPublicWorkspaceListResponse401.from_dict(response.json())



        return response_401

    if response.status_code == 403:
        response_403 = PostPublicWorkspaceListResponse403.from_dict(response.json())



        return response_403

    if response.status_code == 500:
        response_500 = PostPublicWorkspaceListResponse500.from_dict(response.json())



        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[PostPublicWorkspaceListResponse200 | PostPublicWorkspaceListResponse401 | PostPublicWorkspaceListResponse403 | PostPublicWorkspaceListResponse500]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: PostPublicWorkspaceListBody,

) -> Response[PostPublicWorkspaceListResponse200 | PostPublicWorkspaceListResponse401 | PostPublicWorkspaceListResponse403 | PostPublicWorkspaceListResponse500]:
    """ list

     List all workspaces the API key owner is a member of.

    Args:
        body (PostPublicWorkspaceListBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PostPublicWorkspaceListResponse200 | PostPublicWorkspaceListResponse401 | PostPublicWorkspaceListResponse403 | PostPublicWorkspaceListResponse500]
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
    body: PostPublicWorkspaceListBody,

) -> PostPublicWorkspaceListResponse200 | PostPublicWorkspaceListResponse401 | PostPublicWorkspaceListResponse403 | PostPublicWorkspaceListResponse500 | None:
    """ list

     List all workspaces the API key owner is a member of.

    Args:
        body (PostPublicWorkspaceListBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PostPublicWorkspaceListResponse200 | PostPublicWorkspaceListResponse401 | PostPublicWorkspaceListResponse403 | PostPublicWorkspaceListResponse500
     """


    return sync_detailed(
        client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: PostPublicWorkspaceListBody,

) -> Response[PostPublicWorkspaceListResponse200 | PostPublicWorkspaceListResponse401 | PostPublicWorkspaceListResponse403 | PostPublicWorkspaceListResponse500]:
    """ list

     List all workspaces the API key owner is a member of.

    Args:
        body (PostPublicWorkspaceListBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PostPublicWorkspaceListResponse200 | PostPublicWorkspaceListResponse401 | PostPublicWorkspaceListResponse403 | PostPublicWorkspaceListResponse500]
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
    body: PostPublicWorkspaceListBody,

) -> PostPublicWorkspaceListResponse200 | PostPublicWorkspaceListResponse401 | PostPublicWorkspaceListResponse403 | PostPublicWorkspaceListResponse500 | None:
    """ list

     List all workspaces the API key owner is a member of.

    Args:
        body (PostPublicWorkspaceListBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PostPublicWorkspaceListResponse200 | PostPublicWorkspaceListResponse401 | PostPublicWorkspaceListResponse403 | PostPublicWorkspaceListResponse500
     """


    return (await asyncio_detailed(
        client=client,
body=body,

    )).parsed
