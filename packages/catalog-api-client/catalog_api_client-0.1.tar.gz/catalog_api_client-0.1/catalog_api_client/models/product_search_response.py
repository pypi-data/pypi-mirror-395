from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.product_summary import ProductSummary
    from ..models.refinement import Refinement


T = TypeVar("T", bound="ProductSearchResponse")


@_attrs_define
class ProductSearchResponse:
    """This type contains the specifications for the collection of products that match the search or filter criteria of a
    <b>search</b> call. A maximum of 200 product summaries is returned (the result set), fewer if you include the
    <b>limit</b> query parameter in the request.

        Attributes:
            href (str | Unset): This field is reserved for internal or future use. <!-- The URI of the <b>search</b> method
                request that produced this result set. -->
            limit (int | Unset): The number of product summaries returned in the response. This is the <i>result set</i>, a
                subset of the full collection of products that match the search or filter criteria of this call. If the
                <b>limit</b> query parameter was included in the request, this field will have the same value. <br /><br />
                <b>Default:</b> <code>50</code>
            next_ (str | Unset): This field is reserved for internal or future use. <!-- <i>Returned only if</i> there are
                more product records to retrieve from the current collection of matching products, this field contains the
                <b>search</b> call URI for the next result set. For example, the following URI returns records 41 thru 50 from
                the collection of matched products: <br /><br />
                <code><i>path</i>/product_summary/search?limit=10&offset=40</code> <br /><br />  <span
                class="tablenote"><strong>Note:</strong> This feature employs a zero-based list, where the first product in the
                list has an offset of <code>0</code>.</span> -->
            offset (int | Unset): This field is reserved for internal or future use. <!-- The distance (number of records)
                from the first product in the collection to the first product in this result set. If the <b>offset</b> query
                parameter was included in the request, this field will have the same value. The <b>offset</b> value is used in
                conjunction with the <b>limit</b> value to control the pagination of the output. For example, if <b>offset</b>
                is set to <code>30</code> and <b>limit</b> is set to <code>10</code>, the call retrieves products 31 thru 40
                from the resulting collection of products. <br /><br />  <span class="tablenote"><strong>Note:</strong> This
                feature employs a zero-based list, where the first item in the list has an offset of <code>0</code>.</span> <br
                /><br /> <b>Default:</b> <code>0</code> (zero) -->
            prev (str | Unset): This field is reserved for internal or future use.  <!-- <i>Not returned if</i> the
                currently returned result set is the first set of product records from the current collection of matching
                products. This field contains the <b>search</b> call URI for the previous result set. For example, the following
                URI returns products 21 thru 30 from the collection of products: <br /><br />
                <code><i>path</i>/product_summary/search?limit=10&offset=20</code> <br /><br />  <span
                class="tablenote"><strong>Note:</strong> This feature employs a zero-based list, where the first product in the
                list has an offset of <code>0</code>.</span> -->
            product_summaries (list[ProductSummary] | Unset): <i>Returned if</i> the <b>fieldGroups</b> query parameter was
                omitted from the request, or if it was included with a value of <code>MATCHING_PRODUCTS</code> or
                <code>FULL</code>. This container provides an array of product summaries in the current result set for products
                that match the combination of the <b>q</b>, <b>category_ids</b>, and <b>aspect_filter</b> parameters that were
                provided in the request. Each product summary includes information about the product's identifiers, product
                images, aspects, the product page URL, and the <b>getProduct</b> URL for retrieving the product details.
            refinement (Refinement | Unset): This type identifies a product category and the aspects associated with that
                category. Each aspect distribution container returns the distribution of values that have been used for the
                aspect.
            total (int | Unset): This field is reserved for internal or future use. <!-- The total number of product records
                in the returned collection of matched products. -->
    """

    href: str | Unset = UNSET
    limit: int | Unset = UNSET
    next_: str | Unset = UNSET
    offset: int | Unset = UNSET
    prev: str | Unset = UNSET
    product_summaries: list[ProductSummary] | Unset = UNSET
    refinement: Refinement | Unset = UNSET
    total: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        href = self.href

        limit = self.limit

        next_ = self.next_

        offset = self.offset

        prev = self.prev

        product_summaries: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.product_summaries, Unset):
            product_summaries = []
            for product_summaries_item_data in self.product_summaries:
                product_summaries_item = product_summaries_item_data.to_dict()
                product_summaries.append(product_summaries_item)

        refinement: dict[str, Any] | Unset = UNSET
        if not isinstance(self.refinement, Unset):
            refinement = self.refinement.to_dict()

        total = self.total

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if href is not UNSET:
            field_dict["href"] = href
        if limit is not UNSET:
            field_dict["limit"] = limit
        if next_ is not UNSET:
            field_dict["next"] = next_
        if offset is not UNSET:
            field_dict["offset"] = offset
        if prev is not UNSET:
            field_dict["prev"] = prev
        if product_summaries is not UNSET:
            field_dict["productSummaries"] = product_summaries
        if refinement is not UNSET:
            field_dict["refinement"] = refinement
        if total is not UNSET:
            field_dict["total"] = total

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.product_summary import ProductSummary
        from ..models.refinement import Refinement

        d = dict(src_dict)
        href = d.pop("href", UNSET)

        limit = d.pop("limit", UNSET)

        next_ = d.pop("next", UNSET)

        offset = d.pop("offset", UNSET)

        prev = d.pop("prev", UNSET)

        _product_summaries = d.pop("productSummaries", UNSET)
        product_summaries: list[ProductSummary] | Unset = UNSET
        if _product_summaries is not UNSET:
            product_summaries = []
            for product_summaries_item_data in _product_summaries:
                product_summaries_item = ProductSummary.from_dict(product_summaries_item_data)

                product_summaries.append(product_summaries_item)

        _refinement = d.pop("refinement", UNSET)
        refinement: Refinement | Unset
        if isinstance(_refinement, Unset):
            refinement = UNSET
        else:
            refinement = Refinement.from_dict(_refinement)

        total = d.pop("total", UNSET)

        product_search_response = cls(
            href=href,
            limit=limit,
            next_=next_,
            offset=offset,
            prev=prev,
            product_summaries=product_summaries,
            refinement=refinement,
            total=total,
        )

        product_search_response.additional_properties = d
        return product_search_response

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
