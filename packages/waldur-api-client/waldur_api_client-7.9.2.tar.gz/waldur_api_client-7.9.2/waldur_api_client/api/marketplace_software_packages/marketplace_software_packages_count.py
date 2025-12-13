from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.marketplace_software_packages_count_o_item import MarketplaceSoftwarePackagesCountOItem
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    catalog_name: Union[Unset, str] = UNSET,
    catalog_uuid: Union[Unset, UUID] = UNSET,
    catalog_version: Union[Unset, str] = UNSET,
    cpu_family: Union[Unset, str] = UNSET,
    cpu_microarchitecture: Union[Unset, str] = UNSET,
    description: Union[Unset, str] = UNSET,
    has_version: Union[Unset, str] = UNSET,
    name: Union[Unset, str] = UNSET,
    o: Union[Unset, list[MarketplaceSoftwarePackagesCountOItem]] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    query: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["catalog_name"] = catalog_name

    json_catalog_uuid: Union[Unset, str] = UNSET
    if not isinstance(catalog_uuid, Unset):
        json_catalog_uuid = str(catalog_uuid)
    params["catalog_uuid"] = json_catalog_uuid

    params["catalog_version"] = catalog_version

    params["cpu_family"] = cpu_family

    params["cpu_microarchitecture"] = cpu_microarchitecture

    params["description"] = description

    params["has_version"] = has_version

    params["name"] = name

    json_o: Union[Unset, list[str]] = UNSET
    if not isinstance(o, Unset):
        json_o = []
        for o_item_data in o:
            o_item = o_item_data.value
            json_o.append(o_item)

    params["o"] = json_o

    json_offering_uuid: Union[Unset, str] = UNSET
    if not isinstance(offering_uuid, Unset):
        json_offering_uuid = str(offering_uuid)
    params["offering_uuid"] = json_offering_uuid

    params["page"] = page

    params["page_size"] = page_size

    params["query"] = query

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "head",
        "url": "/api/marketplace-software-packages/",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> int:
    if response.status_code == HTTPStatus.OK:
        try:
            return int(response.headers["x-result-count"])
        except KeyError:
            raise errors.UnexpectedStatus(
                response.status_code,
                b"Expected 'X-Result-Count' header for HEAD request, but it was not found.",
                response.url,
            )
        except ValueError:
            count_val = response.headers.get("x-result-count")
            msg = f"Expected 'X-Result-Count' header to be an integer, but got '{count_val}'."
            raise errors.UnexpectedStatus(response.status_code, msg.encode(), response.url)
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[int]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    catalog_name: Union[Unset, str] = UNSET,
    catalog_uuid: Union[Unset, UUID] = UNSET,
    catalog_version: Union[Unset, str] = UNSET,
    cpu_family: Union[Unset, str] = UNSET,
    cpu_microarchitecture: Union[Unset, str] = UNSET,
    description: Union[Unset, str] = UNSET,
    has_version: Union[Unset, str] = UNSET,
    name: Union[Unset, str] = UNSET,
    o: Union[Unset, list[MarketplaceSoftwarePackagesCountOItem]] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    query: Union[Unset, str] = UNSET,
) -> Response[int]:
    """List software packages

     Get number of items in the collection matching the request parameters.

    Args:
        catalog_name (Union[Unset, str]):
        catalog_uuid (Union[Unset, UUID]):
        catalog_version (Union[Unset, str]):
        cpu_family (Union[Unset, str]):
        cpu_microarchitecture (Union[Unset, str]):
        description (Union[Unset, str]):
        has_version (Union[Unset, str]):
        name (Union[Unset, str]):
        o (Union[Unset, list[MarketplaceSoftwarePackagesCountOItem]]):
        offering_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        query (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[int]
    """

    kwargs = _get_kwargs(
        catalog_name=catalog_name,
        catalog_uuid=catalog_uuid,
        catalog_version=catalog_version,
        cpu_family=cpu_family,
        cpu_microarchitecture=cpu_microarchitecture,
        description=description,
        has_version=has_version,
        name=name,
        o=o,
        offering_uuid=offering_uuid,
        page=page,
        page_size=page_size,
        query=query,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    catalog_name: Union[Unset, str] = UNSET,
    catalog_uuid: Union[Unset, UUID] = UNSET,
    catalog_version: Union[Unset, str] = UNSET,
    cpu_family: Union[Unset, str] = UNSET,
    cpu_microarchitecture: Union[Unset, str] = UNSET,
    description: Union[Unset, str] = UNSET,
    has_version: Union[Unset, str] = UNSET,
    name: Union[Unset, str] = UNSET,
    o: Union[Unset, list[MarketplaceSoftwarePackagesCountOItem]] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    query: Union[Unset, str] = UNSET,
) -> int:
    """List software packages

     Get number of items in the collection matching the request parameters.

    Args:
        catalog_name (Union[Unset, str]):
        catalog_uuid (Union[Unset, UUID]):
        catalog_version (Union[Unset, str]):
        cpu_family (Union[Unset, str]):
        cpu_microarchitecture (Union[Unset, str]):
        description (Union[Unset, str]):
        has_version (Union[Unset, str]):
        name (Union[Unset, str]):
        o (Union[Unset, list[MarketplaceSoftwarePackagesCountOItem]]):
        offering_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        query (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        int
    """

    return sync_detailed(
        client=client,
        catalog_name=catalog_name,
        catalog_uuid=catalog_uuid,
        catalog_version=catalog_version,
        cpu_family=cpu_family,
        cpu_microarchitecture=cpu_microarchitecture,
        description=description,
        has_version=has_version,
        name=name,
        o=o,
        offering_uuid=offering_uuid,
        page=page,
        page_size=page_size,
        query=query,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    catalog_name: Union[Unset, str] = UNSET,
    catalog_uuid: Union[Unset, UUID] = UNSET,
    catalog_version: Union[Unset, str] = UNSET,
    cpu_family: Union[Unset, str] = UNSET,
    cpu_microarchitecture: Union[Unset, str] = UNSET,
    description: Union[Unset, str] = UNSET,
    has_version: Union[Unset, str] = UNSET,
    name: Union[Unset, str] = UNSET,
    o: Union[Unset, list[MarketplaceSoftwarePackagesCountOItem]] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    query: Union[Unset, str] = UNSET,
) -> Response[int]:
    """List software packages

     Get number of items in the collection matching the request parameters.

    Args:
        catalog_name (Union[Unset, str]):
        catalog_uuid (Union[Unset, UUID]):
        catalog_version (Union[Unset, str]):
        cpu_family (Union[Unset, str]):
        cpu_microarchitecture (Union[Unset, str]):
        description (Union[Unset, str]):
        has_version (Union[Unset, str]):
        name (Union[Unset, str]):
        o (Union[Unset, list[MarketplaceSoftwarePackagesCountOItem]]):
        offering_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        query (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[int]
    """

    kwargs = _get_kwargs(
        catalog_name=catalog_name,
        catalog_uuid=catalog_uuid,
        catalog_version=catalog_version,
        cpu_family=cpu_family,
        cpu_microarchitecture=cpu_microarchitecture,
        description=description,
        has_version=has_version,
        name=name,
        o=o,
        offering_uuid=offering_uuid,
        page=page,
        page_size=page_size,
        query=query,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    catalog_name: Union[Unset, str] = UNSET,
    catalog_uuid: Union[Unset, UUID] = UNSET,
    catalog_version: Union[Unset, str] = UNSET,
    cpu_family: Union[Unset, str] = UNSET,
    cpu_microarchitecture: Union[Unset, str] = UNSET,
    description: Union[Unset, str] = UNSET,
    has_version: Union[Unset, str] = UNSET,
    name: Union[Unset, str] = UNSET,
    o: Union[Unset, list[MarketplaceSoftwarePackagesCountOItem]] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    query: Union[Unset, str] = UNSET,
) -> int:
    """List software packages

     Get number of items in the collection matching the request parameters.

    Args:
        catalog_name (Union[Unset, str]):
        catalog_uuid (Union[Unset, UUID]):
        catalog_version (Union[Unset, str]):
        cpu_family (Union[Unset, str]):
        cpu_microarchitecture (Union[Unset, str]):
        description (Union[Unset, str]):
        has_version (Union[Unset, str]):
        name (Union[Unset, str]):
        o (Union[Unset, list[MarketplaceSoftwarePackagesCountOItem]]):
        offering_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        query (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        int
    """

    return (
        await asyncio_detailed(
            client=client,
            catalog_name=catalog_name,
            catalog_uuid=catalog_uuid,
            catalog_version=catalog_version,
            cpu_family=cpu_family,
            cpu_microarchitecture=cpu_microarchitecture,
            description=description,
            has_version=has_version,
            name=name,
            o=o,
            offering_uuid=offering_uuid,
            page=page,
            page_size=page_size,
            query=query,
        )
    ).parsed
