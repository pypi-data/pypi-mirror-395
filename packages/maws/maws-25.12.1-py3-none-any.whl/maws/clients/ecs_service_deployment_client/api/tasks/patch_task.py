from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.task_deployment_request import TaskDeploymentRequest
from ...types import Response


def _get_kwargs(
    task: str,
    *,
    body: TaskDeploymentRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": f"/tasks/{task}",
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
    task: str,
    *,
    client: AuthenticatedClient,
    body: TaskDeploymentRequest,
) -> Response[Union[Any, ErrorResponse]]:
    """Update an ECS scheduled task.

     Update an ECS scheduled task.

    Args:
        task (str):
        body (TaskDeploymentRequest): ECS Task Deployment Request.
            Triggered by either scheduled or event pattern.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ErrorResponse]]
    """

    kwargs = _get_kwargs(
        task=task,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    task: str,
    *,
    client: AuthenticatedClient,
    body: TaskDeploymentRequest,
) -> Optional[Union[Any, ErrorResponse]]:
    """Update an ECS scheduled task.

     Update an ECS scheduled task.

    Args:
        task (str):
        body (TaskDeploymentRequest): ECS Task Deployment Request.
            Triggered by either scheduled or event pattern.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ErrorResponse]
    """

    return sync_detailed(
        task=task,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    task: str,
    *,
    client: AuthenticatedClient,
    body: TaskDeploymentRequest,
) -> Response[Union[Any, ErrorResponse]]:
    """Update an ECS scheduled task.

     Update an ECS scheduled task.

    Args:
        task (str):
        body (TaskDeploymentRequest): ECS Task Deployment Request.
            Triggered by either scheduled or event pattern.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ErrorResponse]]
    """

    kwargs = _get_kwargs(
        task=task,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    task: str,
    *,
    client: AuthenticatedClient,
    body: TaskDeploymentRequest,
) -> Optional[Union[Any, ErrorResponse]]:
    """Update an ECS scheduled task.

     Update an ECS scheduled task.

    Args:
        task (str):
        body (TaskDeploymentRequest): ECS Task Deployment Request.
            Triggered by either scheduled or event pattern.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ErrorResponse]
    """

    return (
        await asyncio_detailed(
            task=task,
            client=client,
            body=body,
        )
    ).parsed
