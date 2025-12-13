from http import HTTPStatus
from typing import Any, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.post_public_envelope_add_recipients_body import PostPublicEnvelopeAddRecipientsBody
from ...models.post_public_envelope_add_recipients_response_200 import PostPublicEnvelopeAddRecipientsResponse200
from ...models.post_public_envelope_add_recipients_response_400 import PostPublicEnvelopeAddRecipientsResponse400
from ...models.post_public_envelope_add_recipients_response_401 import PostPublicEnvelopeAddRecipientsResponse401
from ...models.post_public_envelope_add_recipients_response_403 import PostPublicEnvelopeAddRecipientsResponse403
from ...models.post_public_envelope_add_recipients_response_500 import PostPublicEnvelopeAddRecipientsResponse500
from typing import cast



def _get_kwargs(
    *,
    body: PostPublicEnvelopeAddRecipientsBody,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/public/envelope/add-recipients",
    }

    _kwargs["json"] = body.to_dict()


    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> PostPublicEnvelopeAddRecipientsResponse200 | PostPublicEnvelopeAddRecipientsResponse400 | PostPublicEnvelopeAddRecipientsResponse401 | PostPublicEnvelopeAddRecipientsResponse403 | PostPublicEnvelopeAddRecipientsResponse500 | None:
    if response.status_code == 200:
        response_200 = PostPublicEnvelopeAddRecipientsResponse200.from_dict(response.json())



        return response_200

    if response.status_code == 400:
        response_400 = PostPublicEnvelopeAddRecipientsResponse400.from_dict(response.json())



        return response_400

    if response.status_code == 401:
        response_401 = PostPublicEnvelopeAddRecipientsResponse401.from_dict(response.json())



        return response_401

    if response.status_code == 403:
        response_403 = PostPublicEnvelopeAddRecipientsResponse403.from_dict(response.json())



        return response_403

    if response.status_code == 500:
        response_500 = PostPublicEnvelopeAddRecipientsResponse500.from_dict(response.json())



        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[PostPublicEnvelopeAddRecipientsResponse200 | PostPublicEnvelopeAddRecipientsResponse400 | PostPublicEnvelopeAddRecipientsResponse401 | PostPublicEnvelopeAddRecipientsResponse403 | PostPublicEnvelopeAddRecipientsResponse500]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: PostPublicEnvelopeAddRecipientsBody,

) -> Response[PostPublicEnvelopeAddRecipientsResponse200 | PostPublicEnvelopeAddRecipientsResponse400 | PostPublicEnvelopeAddRecipientsResponse401 | PostPublicEnvelopeAddRecipientsResponse403 | PostPublicEnvelopeAddRecipientsResponse500]:
    """ add-recipients

     Add multiple recipients to an envelope

    Args:
        body (PostPublicEnvelopeAddRecipientsBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PostPublicEnvelopeAddRecipientsResponse200 | PostPublicEnvelopeAddRecipientsResponse400 | PostPublicEnvelopeAddRecipientsResponse401 | PostPublicEnvelopeAddRecipientsResponse403 | PostPublicEnvelopeAddRecipientsResponse500]
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
    body: PostPublicEnvelopeAddRecipientsBody,

) -> PostPublicEnvelopeAddRecipientsResponse200 | PostPublicEnvelopeAddRecipientsResponse400 | PostPublicEnvelopeAddRecipientsResponse401 | PostPublicEnvelopeAddRecipientsResponse403 | PostPublicEnvelopeAddRecipientsResponse500 | None:
    """ add-recipients

     Add multiple recipients to an envelope

    Args:
        body (PostPublicEnvelopeAddRecipientsBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PostPublicEnvelopeAddRecipientsResponse200 | PostPublicEnvelopeAddRecipientsResponse400 | PostPublicEnvelopeAddRecipientsResponse401 | PostPublicEnvelopeAddRecipientsResponse403 | PostPublicEnvelopeAddRecipientsResponse500
     """


    return sync_detailed(
        client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: PostPublicEnvelopeAddRecipientsBody,

) -> Response[PostPublicEnvelopeAddRecipientsResponse200 | PostPublicEnvelopeAddRecipientsResponse400 | PostPublicEnvelopeAddRecipientsResponse401 | PostPublicEnvelopeAddRecipientsResponse403 | PostPublicEnvelopeAddRecipientsResponse500]:
    """ add-recipients

     Add multiple recipients to an envelope

    Args:
        body (PostPublicEnvelopeAddRecipientsBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PostPublicEnvelopeAddRecipientsResponse200 | PostPublicEnvelopeAddRecipientsResponse400 | PostPublicEnvelopeAddRecipientsResponse401 | PostPublicEnvelopeAddRecipientsResponse403 | PostPublicEnvelopeAddRecipientsResponse500]
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
    body: PostPublicEnvelopeAddRecipientsBody,

) -> PostPublicEnvelopeAddRecipientsResponse200 | PostPublicEnvelopeAddRecipientsResponse400 | PostPublicEnvelopeAddRecipientsResponse401 | PostPublicEnvelopeAddRecipientsResponse403 | PostPublicEnvelopeAddRecipientsResponse500 | None:
    """ add-recipients

     Add multiple recipients to an envelope

    Args:
        body (PostPublicEnvelopeAddRecipientsBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PostPublicEnvelopeAddRecipientsResponse200 | PostPublicEnvelopeAddRecipientsResponse400 | PostPublicEnvelopeAddRecipientsResponse401 | PostPublicEnvelopeAddRecipientsResponse403 | PostPublicEnvelopeAddRecipientsResponse500
     """


    return (await asyncio_detailed(
        client=client,
body=body,

    )).parsed
