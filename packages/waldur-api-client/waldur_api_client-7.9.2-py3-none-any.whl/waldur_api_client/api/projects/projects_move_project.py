from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.move_project_request import MoveProjectRequest
from ...models.project import Project
from ...models.projects_move_project_response_400 import ProjectsMoveProjectResponse400
from ...types import Response


def _get_kwargs(
    uuid: UUID,
    *,
    body: MoveProjectRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/api/projects/{uuid}/move_project/",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[Project, ProjectsMoveProjectResponse400]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = Project.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = ProjectsMoveProjectResponse400.from_dict(response.json())

        return response_400
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Project, ProjectsMoveProjectResponse400]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    body: MoveProjectRequest,
) -> Response[Union[Project, ProjectsMoveProjectResponse400]]:
    """Move project to another customer

     Moves a project and its associated resources to a different customer. This is a staff-only action.
    You can choose whether to preserve existing project permissions for users.

    Args:
        uuid (UUID):
        body (MoveProjectRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Project, ProjectsMoveProjectResponse400]]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    body: MoveProjectRequest,
) -> Union[Project, ProjectsMoveProjectResponse400]:
    """Move project to another customer

     Moves a project and its associated resources to a different customer. This is a staff-only action.
    You can choose whether to preserve existing project permissions for users.

    Args:
        uuid (UUID):
        body (MoveProjectRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Project, ProjectsMoveProjectResponse400]
    """

    return sync_detailed(
        uuid=uuid,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    body: MoveProjectRequest,
) -> Response[Union[Project, ProjectsMoveProjectResponse400]]:
    """Move project to another customer

     Moves a project and its associated resources to a different customer. This is a staff-only action.
    You can choose whether to preserve existing project permissions for users.

    Args:
        uuid (UUID):
        body (MoveProjectRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Project, ProjectsMoveProjectResponse400]]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    body: MoveProjectRequest,
) -> Union[Project, ProjectsMoveProjectResponse400]:
    """Move project to another customer

     Moves a project and its associated resources to a different customer. This is a staff-only action.
    You can choose whether to preserve existing project permissions for users.

    Args:
        uuid (UUID):
        body (MoveProjectRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Project, ProjectsMoveProjectResponse400]
    """

    return (
        await asyncio_detailed(
            uuid=uuid,
            client=client,
            body=body,
        )
    ).parsed
