from http import HTTPStatus
from typing import Any, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.post_public_envelope_get_proof_body import PostPublicEnvelopeGetProofBody
from ...models.post_public_envelope_get_proof_response_400 import PostPublicEnvelopeGetProofResponse400
from ...models.post_public_envelope_get_proof_response_401 import PostPublicEnvelopeGetProofResponse401
from ...models.post_public_envelope_get_proof_response_403 import PostPublicEnvelopeGetProofResponse403
from ...models.post_public_envelope_get_proof_response_500 import PostPublicEnvelopeGetProofResponse500
from typing import cast



def _get_kwargs(
    *,
    body: PostPublicEnvelopeGetProofBody,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/public/envelope/get-proof",
    }

    _kwargs["json"] = body.to_dict()


    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Any | PostPublicEnvelopeGetProofResponse400 | PostPublicEnvelopeGetProofResponse401 | PostPublicEnvelopeGetProofResponse403 | PostPublicEnvelopeGetProofResponse500 | None:
    if response.status_code == 200:
        response_200 = cast(Any, response.content)
        return response_200

    if response.status_code == 400:
        response_400 = PostPublicEnvelopeGetProofResponse400.from_dict(response.content)



        return response_400

    if response.status_code == 401:
        response_401 = PostPublicEnvelopeGetProofResponse401.from_dict(response.content)



        return response_401

    if response.status_code == 403:
        response_403 = PostPublicEnvelopeGetProofResponse403.from_dict(response.content)



        return response_403

    if response.status_code == 500:
        response_500 = PostPublicEnvelopeGetProofResponse500.from_dict(response.content)



        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Any | PostPublicEnvelopeGetProofResponse400 | PostPublicEnvelopeGetProofResponse401 | PostPublicEnvelopeGetProofResponse403 | PostPublicEnvelopeGetProofResponse500]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: PostPublicEnvelopeGetProofBody,

) -> Response[Any | PostPublicEnvelopeGetProofResponse400 | PostPublicEnvelopeGetProofResponse401 | PostPublicEnvelopeGetProofResponse403 | PostPublicEnvelopeGetProofResponse500]:
    """ get-proof

     Download the proof document for a completed envelope.

    Args:
        body (PostPublicEnvelopeGetProofBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | PostPublicEnvelopeGetProofResponse400 | PostPublicEnvelopeGetProofResponse401 | PostPublicEnvelopeGetProofResponse403 | PostPublicEnvelopeGetProofResponse500]
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
    body: PostPublicEnvelopeGetProofBody,

) -> Any | PostPublicEnvelopeGetProofResponse400 | PostPublicEnvelopeGetProofResponse401 | PostPublicEnvelopeGetProofResponse403 | PostPublicEnvelopeGetProofResponse500 | None:
    """ get-proof

     Download the proof document for a completed envelope.

    Args:
        body (PostPublicEnvelopeGetProofBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | PostPublicEnvelopeGetProofResponse400 | PostPublicEnvelopeGetProofResponse401 | PostPublicEnvelopeGetProofResponse403 | PostPublicEnvelopeGetProofResponse500
     """


    return sync_detailed(
        client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: PostPublicEnvelopeGetProofBody,

) -> Response[Any | PostPublicEnvelopeGetProofResponse400 | PostPublicEnvelopeGetProofResponse401 | PostPublicEnvelopeGetProofResponse403 | PostPublicEnvelopeGetProofResponse500]:
    """ get-proof

     Download the proof document for a completed envelope.

    Args:
        body (PostPublicEnvelopeGetProofBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | PostPublicEnvelopeGetProofResponse400 | PostPublicEnvelopeGetProofResponse401 | PostPublicEnvelopeGetProofResponse403 | PostPublicEnvelopeGetProofResponse500]
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
    body: PostPublicEnvelopeGetProofBody,

) -> Any | PostPublicEnvelopeGetProofResponse400 | PostPublicEnvelopeGetProofResponse401 | PostPublicEnvelopeGetProofResponse403 | PostPublicEnvelopeGetProofResponse500 | None:
    """ get-proof

     Download the proof document for a completed envelope.

    Args:
        body (PostPublicEnvelopeGetProofBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | PostPublicEnvelopeGetProofResponse400 | PostPublicEnvelopeGetProofResponse401 | PostPublicEnvelopeGetProofResponse403 | PostPublicEnvelopeGetProofResponse500
     """


    return (await asyncio_detailed(
        client=client,
body=body,

    )).parsed
