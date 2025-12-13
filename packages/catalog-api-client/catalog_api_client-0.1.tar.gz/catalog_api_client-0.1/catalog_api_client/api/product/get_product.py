from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.product import Product
from ...types import UNSET, Response, Unset


def _get_kwargs(
    epid: str,
    *,
    x_ebay_c_marketplace_id: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_ebay_c_marketplace_id, Unset):
        headers["X-EBAY-C-MARKETPLACE-ID"] = x_ebay_c_marketplace_id

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/product/{epid}".format(
            epid=quote(str(epid), safe=""),
        ),
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Any | Product | None:
    if response.status_code == 200:
        response_200 = Product.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = cast(Any, None)
        return response_400

    if response.status_code == 403:
        response_403 = cast(Any, None)
        return response_403

    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404

    if response.status_code == 500:
        response_500 = cast(Any, None)
        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Any | Product]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    epid: str,
    *,
    client: AuthenticatedClient,
    x_ebay_c_marketplace_id: str | Unset = UNSET,
) -> Response[Any | Product]:
    """This method retrieves details of the catalog product identified by the eBay product identifier
    (ePID) specified in the request. These details include the product's title and description, aspects
    and their values, associated images, applicable category IDs, and any recognized identifiers that
    apply to the product. <br /><br /> For a new listing, you can use the <b>search</b> method to
    identify candidate products on which to base the listing, then use the <b>getProduct</b> method to
    present the full details of those candidate products to the seller to make a a final selection.

    Args:
        epid (str):
        x_ebay_c_marketplace_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | Product]
    """

    kwargs = _get_kwargs(
        epid=epid,
        x_ebay_c_marketplace_id=x_ebay_c_marketplace_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    epid: str,
    *,
    client: AuthenticatedClient,
    x_ebay_c_marketplace_id: str | Unset = UNSET,
) -> Any | Product | None:
    """This method retrieves details of the catalog product identified by the eBay product identifier
    (ePID) specified in the request. These details include the product's title and description, aspects
    and their values, associated images, applicable category IDs, and any recognized identifiers that
    apply to the product. <br /><br /> For a new listing, you can use the <b>search</b> method to
    identify candidate products on which to base the listing, then use the <b>getProduct</b> method to
    present the full details of those candidate products to the seller to make a a final selection.

    Args:
        epid (str):
        x_ebay_c_marketplace_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | Product
    """

    return sync_detailed(
        epid=epid,
        client=client,
        x_ebay_c_marketplace_id=x_ebay_c_marketplace_id,
    ).parsed


async def asyncio_detailed(
    epid: str,
    *,
    client: AuthenticatedClient,
    x_ebay_c_marketplace_id: str | Unset = UNSET,
) -> Response[Any | Product]:
    """This method retrieves details of the catalog product identified by the eBay product identifier
    (ePID) specified in the request. These details include the product's title and description, aspects
    and their values, associated images, applicable category IDs, and any recognized identifiers that
    apply to the product. <br /><br /> For a new listing, you can use the <b>search</b> method to
    identify candidate products on which to base the listing, then use the <b>getProduct</b> method to
    present the full details of those candidate products to the seller to make a a final selection.

    Args:
        epid (str):
        x_ebay_c_marketplace_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | Product]
    """

    kwargs = _get_kwargs(
        epid=epid,
        x_ebay_c_marketplace_id=x_ebay_c_marketplace_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    epid: str,
    *,
    client: AuthenticatedClient,
    x_ebay_c_marketplace_id: str | Unset = UNSET,
) -> Any | Product | None:
    """This method retrieves details of the catalog product identified by the eBay product identifier
    (ePID) specified in the request. These details include the product's title and description, aspects
    and their values, associated images, applicable category IDs, and any recognized identifiers that
    apply to the product. <br /><br /> For a new listing, you can use the <b>search</b> method to
    identify candidate products on which to base the listing, then use the <b>getProduct</b> method to
    present the full details of those candidate products to the seller to make a a final selection.

    Args:
        epid (str):
        x_ebay_c_marketplace_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | Product
    """

    return (
        await asyncio_detailed(
            epid=epid,
            client=client,
            x_ebay_c_marketplace_id=x_ebay_c_marketplace_id,
        )
    ).parsed
