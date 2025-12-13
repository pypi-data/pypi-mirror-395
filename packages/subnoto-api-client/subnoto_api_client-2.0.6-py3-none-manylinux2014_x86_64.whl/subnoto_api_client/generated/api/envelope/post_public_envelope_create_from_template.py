from http import HTTPStatus
from typing import Any, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.post_public_envelope_create_from_template_body import PostPublicEnvelopeCreateFromTemplateBody
from ...models.post_public_envelope_create_from_template_response_200 import PostPublicEnvelopeCreateFromTemplateResponse200
from ...models.post_public_envelope_create_from_template_response_400 import PostPublicEnvelopeCreateFromTemplateResponse400
from ...models.post_public_envelope_create_from_template_response_401 import PostPublicEnvelopeCreateFromTemplateResponse401
from ...models.post_public_envelope_create_from_template_response_403 import PostPublicEnvelopeCreateFromTemplateResponse403
from ...models.post_public_envelope_create_from_template_response_500 import PostPublicEnvelopeCreateFromTemplateResponse500
from typing import cast



def _get_kwargs(
    *,
    body: PostPublicEnvelopeCreateFromTemplateBody,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/public/envelope/create-from-template",
    }

    _kwargs["json"] = body.to_dict()


    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> PostPublicEnvelopeCreateFromTemplateResponse200 | PostPublicEnvelopeCreateFromTemplateResponse400 | PostPublicEnvelopeCreateFromTemplateResponse401 | PostPublicEnvelopeCreateFromTemplateResponse403 | PostPublicEnvelopeCreateFromTemplateResponse500 | None:
    if response.status_code == 200:
        response_200 = PostPublicEnvelopeCreateFromTemplateResponse200.from_dict(response.json())



        return response_200

    if response.status_code == 400:
        response_400 = PostPublicEnvelopeCreateFromTemplateResponse400.from_dict(response.json())



        return response_400

    if response.status_code == 401:
        response_401 = PostPublicEnvelopeCreateFromTemplateResponse401.from_dict(response.json())



        return response_401

    if response.status_code == 403:
        response_403 = PostPublicEnvelopeCreateFromTemplateResponse403.from_dict(response.json())



        return response_403

    if response.status_code == 500:
        response_500 = PostPublicEnvelopeCreateFromTemplateResponse500.from_dict(response.json())



        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[PostPublicEnvelopeCreateFromTemplateResponse200 | PostPublicEnvelopeCreateFromTemplateResponse400 | PostPublicEnvelopeCreateFromTemplateResponse401 | PostPublicEnvelopeCreateFromTemplateResponse403 | PostPublicEnvelopeCreateFromTemplateResponse500]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: PostPublicEnvelopeCreateFromTemplateBody,

) -> Response[PostPublicEnvelopeCreateFromTemplateResponse200 | PostPublicEnvelopeCreateFromTemplateResponse400 | PostPublicEnvelopeCreateFromTemplateResponse401 | PostPublicEnvelopeCreateFromTemplateResponse403 | PostPublicEnvelopeCreateFromTemplateResponse500]:
    """ create-from-template

     Create a new envelope from a template by copying documents and mapping recipient labels to actual
    recipients

    Args:
        body (PostPublicEnvelopeCreateFromTemplateBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PostPublicEnvelopeCreateFromTemplateResponse200 | PostPublicEnvelopeCreateFromTemplateResponse400 | PostPublicEnvelopeCreateFromTemplateResponse401 | PostPublicEnvelopeCreateFromTemplateResponse403 | PostPublicEnvelopeCreateFromTemplateResponse500]
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
    body: PostPublicEnvelopeCreateFromTemplateBody,

) -> PostPublicEnvelopeCreateFromTemplateResponse200 | PostPublicEnvelopeCreateFromTemplateResponse400 | PostPublicEnvelopeCreateFromTemplateResponse401 | PostPublicEnvelopeCreateFromTemplateResponse403 | PostPublicEnvelopeCreateFromTemplateResponse500 | None:
    """ create-from-template

     Create a new envelope from a template by copying documents and mapping recipient labels to actual
    recipients

    Args:
        body (PostPublicEnvelopeCreateFromTemplateBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PostPublicEnvelopeCreateFromTemplateResponse200 | PostPublicEnvelopeCreateFromTemplateResponse400 | PostPublicEnvelopeCreateFromTemplateResponse401 | PostPublicEnvelopeCreateFromTemplateResponse403 | PostPublicEnvelopeCreateFromTemplateResponse500
     """


    return sync_detailed(
        client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: PostPublicEnvelopeCreateFromTemplateBody,

) -> Response[PostPublicEnvelopeCreateFromTemplateResponse200 | PostPublicEnvelopeCreateFromTemplateResponse400 | PostPublicEnvelopeCreateFromTemplateResponse401 | PostPublicEnvelopeCreateFromTemplateResponse403 | PostPublicEnvelopeCreateFromTemplateResponse500]:
    """ create-from-template

     Create a new envelope from a template by copying documents and mapping recipient labels to actual
    recipients

    Args:
        body (PostPublicEnvelopeCreateFromTemplateBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PostPublicEnvelopeCreateFromTemplateResponse200 | PostPublicEnvelopeCreateFromTemplateResponse400 | PostPublicEnvelopeCreateFromTemplateResponse401 | PostPublicEnvelopeCreateFromTemplateResponse403 | PostPublicEnvelopeCreateFromTemplateResponse500]
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
    body: PostPublicEnvelopeCreateFromTemplateBody,

) -> PostPublicEnvelopeCreateFromTemplateResponse200 | PostPublicEnvelopeCreateFromTemplateResponse400 | PostPublicEnvelopeCreateFromTemplateResponse401 | PostPublicEnvelopeCreateFromTemplateResponse403 | PostPublicEnvelopeCreateFromTemplateResponse500 | None:
    """ create-from-template

     Create a new envelope from a template by copying documents and mapping recipient labels to actual
    recipients

    Args:
        body (PostPublicEnvelopeCreateFromTemplateBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PostPublicEnvelopeCreateFromTemplateResponse200 | PostPublicEnvelopeCreateFromTemplateResponse400 | PostPublicEnvelopeCreateFromTemplateResponse401 | PostPublicEnvelopeCreateFromTemplateResponse403 | PostPublicEnvelopeCreateFromTemplateResponse500
     """


    return (await asyncio_detailed(
        client=client,
body=body,

    )).parsed
