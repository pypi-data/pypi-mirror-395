from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response_400 import ErrorResponse400
from ...models.github_device_flow_start_response import GithubDeviceFlowStartResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    invite_code: Union[None, Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_invite_code: Union[None, Unset, str]
    if isinstance(invite_code, Unset):
        json_invite_code = UNSET
    else:
        json_invite_code = invite_code
    params["invite_code"] = json_invite_code

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v1/github/device-flow/code",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[ErrorResponse400, GithubDeviceFlowStartResponse]]:
    if response.status_code == 201:
        response_201 = GithubDeviceFlowStartResponse.from_dict(response.json())

        return response_201

    if response.status_code == 400:
        response_400 = ErrorResponse400.from_dict(response.json())

        return response_400

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[ErrorResponse400, GithubDeviceFlowStartResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    invite_code: Union[None, Unset, str] = UNSET,
) -> Response[Union[ErrorResponse400, GithubDeviceFlowStartResponse]]:
    """GithubOauthStart

    Args:
        invite_code (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse400, GithubDeviceFlowStartResponse]]
    """

    kwargs = _get_kwargs(
        invite_code=invite_code,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    invite_code: Union[None, Unset, str] = UNSET,
) -> Optional[Union[ErrorResponse400, GithubDeviceFlowStartResponse]]:
    """GithubOauthStart

    Args:
        invite_code (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse400, GithubDeviceFlowStartResponse]
    """

    return sync_detailed(
        client=client,
        invite_code=invite_code,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    invite_code: Union[None, Unset, str] = UNSET,
) -> Response[Union[ErrorResponse400, GithubDeviceFlowStartResponse]]:
    """GithubOauthStart

    Args:
        invite_code (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse400, GithubDeviceFlowStartResponse]]
    """

    kwargs = _get_kwargs(
        invite_code=invite_code,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    invite_code: Union[None, Unset, str] = UNSET,
) -> Optional[Union[ErrorResponse400, GithubDeviceFlowStartResponse]]:
    """GithubOauthStart

    Args:
        invite_code (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse400, GithubDeviceFlowStartResponse]
    """

    return (
        await asyncio_detailed(
            client=client,
            invite_code=invite_code,
        )
    ).parsed
