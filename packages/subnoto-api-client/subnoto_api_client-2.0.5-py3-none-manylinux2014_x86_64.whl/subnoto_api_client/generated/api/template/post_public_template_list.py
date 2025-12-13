from http import HTTPStatus
from typing import Any, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.post_public_template_list_body import PostPublicTemplateListBody
from ...models.post_public_template_list_response_200 import PostPublicTemplateListResponse200
from ...models.post_public_template_list_response_401 import PostPublicTemplateListResponse401
from ...models.post_public_template_list_response_403 import PostPublicTemplateListResponse403
from ...models.post_public_template_list_response_500 import PostPublicTemplateListResponse500
from typing import cast



def _get_kwargs(
    *,
    body: PostPublicTemplateListBody,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/public/template/list",
    }

    _kwargs["json"] = body.to_dict()


    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> PostPublicTemplateListResponse200 | PostPublicTemplateListResponse401 | PostPublicTemplateListResponse403 | PostPublicTemplateListResponse500 | None:
    if response.status_code == 200:
        response_200 = PostPublicTemplateListResponse200.from_dict(response.json())



        return response_200

    if response.status_code == 401:
        response_401 = PostPublicTemplateListResponse401.from_dict(response.json())



        return response_401

    if response.status_code == 403:
        response_403 = PostPublicTemplateListResponse403.from_dict(response.json())



        return response_403

    if response.status_code == 500:
        response_500 = PostPublicTemplateListResponse500.from_dict(response.json())



        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[PostPublicTemplateListResponse200 | PostPublicTemplateListResponse401 | PostPublicTemplateListResponse403 | PostPublicTemplateListResponse500]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: PostPublicTemplateListBody,

) -> Response[PostPublicTemplateListResponse200 | PostPublicTemplateListResponse401 | PostPublicTemplateListResponse403 | PostPublicTemplateListResponse500]:
    """ list

     List all templates accessible by the team.

    Args:
        body (PostPublicTemplateListBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PostPublicTemplateListResponse200 | PostPublicTemplateListResponse401 | PostPublicTemplateListResponse403 | PostPublicTemplateListResponse500]
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
    body: PostPublicTemplateListBody,

) -> PostPublicTemplateListResponse200 | PostPublicTemplateListResponse401 | PostPublicTemplateListResponse403 | PostPublicTemplateListResponse500 | None:
    """ list

     List all templates accessible by the team.

    Args:
        body (PostPublicTemplateListBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PostPublicTemplateListResponse200 | PostPublicTemplateListResponse401 | PostPublicTemplateListResponse403 | PostPublicTemplateListResponse500
     """


    return sync_detailed(
        client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: PostPublicTemplateListBody,

) -> Response[PostPublicTemplateListResponse200 | PostPublicTemplateListResponse401 | PostPublicTemplateListResponse403 | PostPublicTemplateListResponse500]:
    """ list

     List all templates accessible by the team.

    Args:
        body (PostPublicTemplateListBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PostPublicTemplateListResponse200 | PostPublicTemplateListResponse401 | PostPublicTemplateListResponse403 | PostPublicTemplateListResponse500]
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
    body: PostPublicTemplateListBody,

) -> PostPublicTemplateListResponse200 | PostPublicTemplateListResponse401 | PostPublicTemplateListResponse403 | PostPublicTemplateListResponse500 | None:
    """ list

     List all templates accessible by the team.

    Args:
        body (PostPublicTemplateListBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PostPublicTemplateListResponse200 | PostPublicTemplateListResponse401 | PostPublicTemplateListResponse403 | PostPublicTemplateListResponse500
     """


    return (await asyncio_detailed(
        client=client,
body=body,

    )).parsed
