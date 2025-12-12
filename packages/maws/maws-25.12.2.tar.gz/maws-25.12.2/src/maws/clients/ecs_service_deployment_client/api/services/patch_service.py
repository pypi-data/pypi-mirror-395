from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.service_deployment_request import ServiceDeploymentRequest
from ...types import Response


def _get_kwargs(
    service: str,
    *,
    body: ServiceDeploymentRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": f"/services/{service}",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, ErrorResponse]]:
    if response.status_code == 201:
        response_201 = cast(Any, None)
        return response_201
    if response.status_code == 403:
        response_403 = cast(Any, None)
        return response_403
    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404
    if response.status_code == 417:
        response_417 = ErrorResponse.from_dict(response.json())

        return response_417
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, ErrorResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    service: str,
    *,
    client: AuthenticatedClient,
    body: ServiceDeploymentRequest,
) -> Response[Union[Any, ErrorResponse]]:
    """Update an ECS service.

     Update an ECS service.

    Args:
        service (str):
        body (ServiceDeploymentRequest): ECS Service Deployment Request.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ErrorResponse]]
    """

    kwargs = _get_kwargs(
        service=service,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    service: str,
    *,
    client: AuthenticatedClient,
    body: ServiceDeploymentRequest,
) -> Optional[Union[Any, ErrorResponse]]:
    """Update an ECS service.

     Update an ECS service.

    Args:
        service (str):
        body (ServiceDeploymentRequest): ECS Service Deployment Request.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ErrorResponse]
    """

    return sync_detailed(
        service=service,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    service: str,
    *,
    client: AuthenticatedClient,
    body: ServiceDeploymentRequest,
) -> Response[Union[Any, ErrorResponse]]:
    """Update an ECS service.

     Update an ECS service.

    Args:
        service (str):
        body (ServiceDeploymentRequest): ECS Service Deployment Request.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ErrorResponse]]
    """

    kwargs = _get_kwargs(
        service=service,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    service: str,
    *,
    client: AuthenticatedClient,
    body: ServiceDeploymentRequest,
) -> Optional[Union[Any, ErrorResponse]]:
    """Update an ECS service.

     Update an ECS service.

    Args:
        service (str):
        body (ServiceDeploymentRequest): ECS Service Deployment Request.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ErrorResponse]
    """

    return (
        await asyncio_detailed(
            service=service,
            client=client,
            body=body,
        )
    ).parsed
