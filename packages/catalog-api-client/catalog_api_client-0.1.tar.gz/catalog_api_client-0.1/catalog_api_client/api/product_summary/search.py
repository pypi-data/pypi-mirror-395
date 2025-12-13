from http import HTTPStatus
from typing import Any, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.product_search_response import ProductSearchResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    aspect_filter: str | Unset = UNSET,
    category_ids: str | Unset = UNSET,
    fieldgroups: str | Unset = UNSET,
    gtin: str | Unset = UNSET,
    limit: str | Unset = UNSET,
    mpn: str | Unset = UNSET,
    offset: str | Unset = UNSET,
    q: str | Unset = UNSET,
    x_ebay_c_marketplace_id: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_ebay_c_marketplace_id, Unset):
        headers["X-EBAY-C-MARKETPLACE-ID"] = x_ebay_c_marketplace_id

    params: dict[str, Any] = {}

    params["aspect_filter"] = aspect_filter

    params["category_ids"] = category_ids

    params["fieldgroups"] = fieldgroups

    params["gtin"] = gtin

    params["limit"] = limit

    params["mpn"] = mpn

    params["offset"] = offset

    params["q"] = q

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/product_summary/search",
        "params": params,
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | ProductSearchResponse | None:
    if response.status_code == 200:
        response_200 = ProductSearchResponse.from_dict(response.json())

        return response_200

    if response.status_code == 204:
        response_204 = cast(Any, None)
        return response_204

    if response.status_code == 400:
        response_400 = cast(Any, None)
        return response_400

    if response.status_code == 403:
        response_403 = cast(Any, None)
        return response_403

    if response.status_code == 500:
        response_500 = cast(Any, None)
        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Any | ProductSearchResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    aspect_filter: str | Unset = UNSET,
    category_ids: str | Unset = UNSET,
    fieldgroups: str | Unset = UNSET,
    gtin: str | Unset = UNSET,
    limit: str | Unset = UNSET,
    mpn: str | Unset = UNSET,
    offset: str | Unset = UNSET,
    q: str | Unset = UNSET,
    x_ebay_c_marketplace_id: str | Unset = UNSET,
) -> Response[Any | ProductSearchResponse]:
    r"""This method searches for and retrieves summaries of one or more products in the eBay catalog that
    match the search criteria provided by a seller. The seller can use the summaries to select the
    product in the eBay catalog that corresponds to the item that the seller wants to offer for sale.
    When a corresponding product is found and adopted by the seller, eBay will use the product
    information to populate the item listing. The criteria supported by <b>search</b> include keywords,
    product categories, and category aspects. To see the full details of a selected product, use the
    <b>getProduct</b> call. <br /><br /> In addition to product summaries, this method can also be used
    to identify <i>refinements</i>, which help you to better pinpoint the product you're looking for. A
    refinement consists of one or more <i>aspect</i> values and a count of the number of times that each
    value has been used in previous eBay listings. An aspect is a property (e.g. color or size) of an
    eBay category, used by sellers to provide details about the items they're listing. The
    <b>refinement</b> container is returned when you include the <b>fieldGroups</b> query parameter in
    the request with a value of <code>ASPECT_REFINEMENTS</code> or <code>FULL</code>. <br /><br /> <span
    style=\"padding: 15px 20px; display: block; border: 1px solid #cccccc\"><b>Example</b> <br />A
    seller wants to find a product that is \"gray\" in color, but doesn't know what term the
    manufacturer uses for that color. It might be <code>Silver</code>, <code>Brushed Nickel</code>,
    <code>Pewter</code>, or even <code>Grey</code>. The returned <b>refinement</b> container identifies
    all aspects that have been used in past listings for products that match your search criteria, along
    with all of the values those aspects have taken, and the number of times each value was used. You
    can use this data to present the seller with a histogram of the values of each aspect. The seller
    can see which color values have been used in the past, and how frequently they have been used, and
    selects the most likely value or values for their product. You issue the <b>search</b> method again
    with those values in the <b>aspect_filter</b> parameter to narrow down the collection of products
    returned by the call.</span> <br /><br /> Although all query parameters are optional, this method
    must include at least the <b>q</b> parameter, or the <b>category_ids</b>, <b>gtin</b>, or <b>mpn</b>
    parameter with a valid value. If you provide more than one of these parameters, they will be
    combined with a logical AND to further refine the returned collection of matching products. <br
    /><br /> <span class=\"tablenote\"><strong>Note:</strong> This method requires that certain special
    characters in the query parameters be percent-encoded: <br /><br />
    &nbsp;&nbsp;&nbsp;&nbsp;<code>(space)</code> = <code>%20</code>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<code>,</code> = <code>%2C</code>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<code>:</code> = <code>%3A</code>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<code>[</code> = <code>%5B</code>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<code>]</code> = <code>%5D</code>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<code>{</code> = <code>%7B</code>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<code>|</code> = <code>%7C</code>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<code>}</code> = <code>%7D</code> <br /><br /> This requirement
    applies to all query parameter values. However, for readability, method examples and samples in this
    documentation will not use the encoding.</span> <br /><br /> This method returns product summaries
    rather than the full details of the products. To retrieve the full details of a product, use the
    <b>getProduct</b> method with an ePID.

    Args:
        aspect_filter (str | Unset):
        category_ids (str | Unset):
        fieldgroups (str | Unset):
        gtin (str | Unset):
        limit (str | Unset):
        mpn (str | Unset):
        offset (str | Unset):
        q (str | Unset):
        x_ebay_c_marketplace_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ProductSearchResponse]
    """

    kwargs = _get_kwargs(
        aspect_filter=aspect_filter,
        category_ids=category_ids,
        fieldgroups=fieldgroups,
        gtin=gtin,
        limit=limit,
        mpn=mpn,
        offset=offset,
        q=q,
        x_ebay_c_marketplace_id=x_ebay_c_marketplace_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    aspect_filter: str | Unset = UNSET,
    category_ids: str | Unset = UNSET,
    fieldgroups: str | Unset = UNSET,
    gtin: str | Unset = UNSET,
    limit: str | Unset = UNSET,
    mpn: str | Unset = UNSET,
    offset: str | Unset = UNSET,
    q: str | Unset = UNSET,
    x_ebay_c_marketplace_id: str | Unset = UNSET,
) -> Any | ProductSearchResponse | None:
    r"""This method searches for and retrieves summaries of one or more products in the eBay catalog that
    match the search criteria provided by a seller. The seller can use the summaries to select the
    product in the eBay catalog that corresponds to the item that the seller wants to offer for sale.
    When a corresponding product is found and adopted by the seller, eBay will use the product
    information to populate the item listing. The criteria supported by <b>search</b> include keywords,
    product categories, and category aspects. To see the full details of a selected product, use the
    <b>getProduct</b> call. <br /><br /> In addition to product summaries, this method can also be used
    to identify <i>refinements</i>, which help you to better pinpoint the product you're looking for. A
    refinement consists of one or more <i>aspect</i> values and a count of the number of times that each
    value has been used in previous eBay listings. An aspect is a property (e.g. color or size) of an
    eBay category, used by sellers to provide details about the items they're listing. The
    <b>refinement</b> container is returned when you include the <b>fieldGroups</b> query parameter in
    the request with a value of <code>ASPECT_REFINEMENTS</code> or <code>FULL</code>. <br /><br /> <span
    style=\"padding: 15px 20px; display: block; border: 1px solid #cccccc\"><b>Example</b> <br />A
    seller wants to find a product that is \"gray\" in color, but doesn't know what term the
    manufacturer uses for that color. It might be <code>Silver</code>, <code>Brushed Nickel</code>,
    <code>Pewter</code>, or even <code>Grey</code>. The returned <b>refinement</b> container identifies
    all aspects that have been used in past listings for products that match your search criteria, along
    with all of the values those aspects have taken, and the number of times each value was used. You
    can use this data to present the seller with a histogram of the values of each aspect. The seller
    can see which color values have been used in the past, and how frequently they have been used, and
    selects the most likely value or values for their product. You issue the <b>search</b> method again
    with those values in the <b>aspect_filter</b> parameter to narrow down the collection of products
    returned by the call.</span> <br /><br /> Although all query parameters are optional, this method
    must include at least the <b>q</b> parameter, or the <b>category_ids</b>, <b>gtin</b>, or <b>mpn</b>
    parameter with a valid value. If you provide more than one of these parameters, they will be
    combined with a logical AND to further refine the returned collection of matching products. <br
    /><br /> <span class=\"tablenote\"><strong>Note:</strong> This method requires that certain special
    characters in the query parameters be percent-encoded: <br /><br />
    &nbsp;&nbsp;&nbsp;&nbsp;<code>(space)</code> = <code>%20</code>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<code>,</code> = <code>%2C</code>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<code>:</code> = <code>%3A</code>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<code>[</code> = <code>%5B</code>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<code>]</code> = <code>%5D</code>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<code>{</code> = <code>%7B</code>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<code>|</code> = <code>%7C</code>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<code>}</code> = <code>%7D</code> <br /><br /> This requirement
    applies to all query parameter values. However, for readability, method examples and samples in this
    documentation will not use the encoding.</span> <br /><br /> This method returns product summaries
    rather than the full details of the products. To retrieve the full details of a product, use the
    <b>getProduct</b> method with an ePID.

    Args:
        aspect_filter (str | Unset):
        category_ids (str | Unset):
        fieldgroups (str | Unset):
        gtin (str | Unset):
        limit (str | Unset):
        mpn (str | Unset):
        offset (str | Unset):
        q (str | Unset):
        x_ebay_c_marketplace_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | ProductSearchResponse
    """

    return sync_detailed(
        client=client,
        aspect_filter=aspect_filter,
        category_ids=category_ids,
        fieldgroups=fieldgroups,
        gtin=gtin,
        limit=limit,
        mpn=mpn,
        offset=offset,
        q=q,
        x_ebay_c_marketplace_id=x_ebay_c_marketplace_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    aspect_filter: str | Unset = UNSET,
    category_ids: str | Unset = UNSET,
    fieldgroups: str | Unset = UNSET,
    gtin: str | Unset = UNSET,
    limit: str | Unset = UNSET,
    mpn: str | Unset = UNSET,
    offset: str | Unset = UNSET,
    q: str | Unset = UNSET,
    x_ebay_c_marketplace_id: str | Unset = UNSET,
) -> Response[Any | ProductSearchResponse]:
    r"""This method searches for and retrieves summaries of one or more products in the eBay catalog that
    match the search criteria provided by a seller. The seller can use the summaries to select the
    product in the eBay catalog that corresponds to the item that the seller wants to offer for sale.
    When a corresponding product is found and adopted by the seller, eBay will use the product
    information to populate the item listing. The criteria supported by <b>search</b> include keywords,
    product categories, and category aspects. To see the full details of a selected product, use the
    <b>getProduct</b> call. <br /><br /> In addition to product summaries, this method can also be used
    to identify <i>refinements</i>, which help you to better pinpoint the product you're looking for. A
    refinement consists of one or more <i>aspect</i> values and a count of the number of times that each
    value has been used in previous eBay listings. An aspect is a property (e.g. color or size) of an
    eBay category, used by sellers to provide details about the items they're listing. The
    <b>refinement</b> container is returned when you include the <b>fieldGroups</b> query parameter in
    the request with a value of <code>ASPECT_REFINEMENTS</code> or <code>FULL</code>. <br /><br /> <span
    style=\"padding: 15px 20px; display: block; border: 1px solid #cccccc\"><b>Example</b> <br />A
    seller wants to find a product that is \"gray\" in color, but doesn't know what term the
    manufacturer uses for that color. It might be <code>Silver</code>, <code>Brushed Nickel</code>,
    <code>Pewter</code>, or even <code>Grey</code>. The returned <b>refinement</b> container identifies
    all aspects that have been used in past listings for products that match your search criteria, along
    with all of the values those aspects have taken, and the number of times each value was used. You
    can use this data to present the seller with a histogram of the values of each aspect. The seller
    can see which color values have been used in the past, and how frequently they have been used, and
    selects the most likely value or values for their product. You issue the <b>search</b> method again
    with those values in the <b>aspect_filter</b> parameter to narrow down the collection of products
    returned by the call.</span> <br /><br /> Although all query parameters are optional, this method
    must include at least the <b>q</b> parameter, or the <b>category_ids</b>, <b>gtin</b>, or <b>mpn</b>
    parameter with a valid value. If you provide more than one of these parameters, they will be
    combined with a logical AND to further refine the returned collection of matching products. <br
    /><br /> <span class=\"tablenote\"><strong>Note:</strong> This method requires that certain special
    characters in the query parameters be percent-encoded: <br /><br />
    &nbsp;&nbsp;&nbsp;&nbsp;<code>(space)</code> = <code>%20</code>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<code>,</code> = <code>%2C</code>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<code>:</code> = <code>%3A</code>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<code>[</code> = <code>%5B</code>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<code>]</code> = <code>%5D</code>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<code>{</code> = <code>%7B</code>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<code>|</code> = <code>%7C</code>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<code>}</code> = <code>%7D</code> <br /><br /> This requirement
    applies to all query parameter values. However, for readability, method examples and samples in this
    documentation will not use the encoding.</span> <br /><br /> This method returns product summaries
    rather than the full details of the products. To retrieve the full details of a product, use the
    <b>getProduct</b> method with an ePID.

    Args:
        aspect_filter (str | Unset):
        category_ids (str | Unset):
        fieldgroups (str | Unset):
        gtin (str | Unset):
        limit (str | Unset):
        mpn (str | Unset):
        offset (str | Unset):
        q (str | Unset):
        x_ebay_c_marketplace_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ProductSearchResponse]
    """

    kwargs = _get_kwargs(
        aspect_filter=aspect_filter,
        category_ids=category_ids,
        fieldgroups=fieldgroups,
        gtin=gtin,
        limit=limit,
        mpn=mpn,
        offset=offset,
        q=q,
        x_ebay_c_marketplace_id=x_ebay_c_marketplace_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    aspect_filter: str | Unset = UNSET,
    category_ids: str | Unset = UNSET,
    fieldgroups: str | Unset = UNSET,
    gtin: str | Unset = UNSET,
    limit: str | Unset = UNSET,
    mpn: str | Unset = UNSET,
    offset: str | Unset = UNSET,
    q: str | Unset = UNSET,
    x_ebay_c_marketplace_id: str | Unset = UNSET,
) -> Any | ProductSearchResponse | None:
    r"""This method searches for and retrieves summaries of one or more products in the eBay catalog that
    match the search criteria provided by a seller. The seller can use the summaries to select the
    product in the eBay catalog that corresponds to the item that the seller wants to offer for sale.
    When a corresponding product is found and adopted by the seller, eBay will use the product
    information to populate the item listing. The criteria supported by <b>search</b> include keywords,
    product categories, and category aspects. To see the full details of a selected product, use the
    <b>getProduct</b> call. <br /><br /> In addition to product summaries, this method can also be used
    to identify <i>refinements</i>, which help you to better pinpoint the product you're looking for. A
    refinement consists of one or more <i>aspect</i> values and a count of the number of times that each
    value has been used in previous eBay listings. An aspect is a property (e.g. color or size) of an
    eBay category, used by sellers to provide details about the items they're listing. The
    <b>refinement</b> container is returned when you include the <b>fieldGroups</b> query parameter in
    the request with a value of <code>ASPECT_REFINEMENTS</code> or <code>FULL</code>. <br /><br /> <span
    style=\"padding: 15px 20px; display: block; border: 1px solid #cccccc\"><b>Example</b> <br />A
    seller wants to find a product that is \"gray\" in color, but doesn't know what term the
    manufacturer uses for that color. It might be <code>Silver</code>, <code>Brushed Nickel</code>,
    <code>Pewter</code>, or even <code>Grey</code>. The returned <b>refinement</b> container identifies
    all aspects that have been used in past listings for products that match your search criteria, along
    with all of the values those aspects have taken, and the number of times each value was used. You
    can use this data to present the seller with a histogram of the values of each aspect. The seller
    can see which color values have been used in the past, and how frequently they have been used, and
    selects the most likely value or values for their product. You issue the <b>search</b> method again
    with those values in the <b>aspect_filter</b> parameter to narrow down the collection of products
    returned by the call.</span> <br /><br /> Although all query parameters are optional, this method
    must include at least the <b>q</b> parameter, or the <b>category_ids</b>, <b>gtin</b>, or <b>mpn</b>
    parameter with a valid value. If you provide more than one of these parameters, they will be
    combined with a logical AND to further refine the returned collection of matching products. <br
    /><br /> <span class=\"tablenote\"><strong>Note:</strong> This method requires that certain special
    characters in the query parameters be percent-encoded: <br /><br />
    &nbsp;&nbsp;&nbsp;&nbsp;<code>(space)</code> = <code>%20</code>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<code>,</code> = <code>%2C</code>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<code>:</code> = <code>%3A</code>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<code>[</code> = <code>%5B</code>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<code>]</code> = <code>%5D</code>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<code>{</code> = <code>%7B</code>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<code>|</code> = <code>%7C</code>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<code>}</code> = <code>%7D</code> <br /><br /> This requirement
    applies to all query parameter values. However, for readability, method examples and samples in this
    documentation will not use the encoding.</span> <br /><br /> This method returns product summaries
    rather than the full details of the products. To retrieve the full details of a product, use the
    <b>getProduct</b> method with an ePID.

    Args:
        aspect_filter (str | Unset):
        category_ids (str | Unset):
        fieldgroups (str | Unset):
        gtin (str | Unset):
        limit (str | Unset):
        mpn (str | Unset):
        offset (str | Unset):
        q (str | Unset):
        x_ebay_c_marketplace_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | ProductSearchResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            aspect_filter=aspect_filter,
            category_ids=category_ids,
            fieldgroups=fieldgroups,
            gtin=gtin,
            limit=limit,
            mpn=mpn,
            offset=offset,
            q=q,
            x_ebay_c_marketplace_id=x_ebay_c_marketplace_id,
        )
    ).parsed
