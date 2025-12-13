from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="AspectValueDistribution")


@_attrs_define
class AspectValueDistribution:
    """This type contains information about one value of a specified aspect. This value serves as a product refinement.

    Attributes:
        localized_aspect_value (str | Unset): The localized value of the category aspect identified by
            <b>refinement.aspectDistributions.localizedAspectName</b>.
        match_count (int | Unset): The number of times the value of <b>localizedAspectValue</b> has been used for eBay
            product listings. By comparing this quantity to the <b>matchCount</b> for other values of the same aspect, you
            can present a histogram of the values to sellers, who can use that information to select which aspect value is
            most appropriate for their product. You can then include the user-selected value in the the <b>search</b> call's
            <b>aspect_filter</b> parameter to refine your search.
        refinement_href (str | Unset): A HATEOAS reference that further refines the search with this particular
            <b>localizedAspectValue</b>.
    """

    localized_aspect_value: str | Unset = UNSET
    match_count: int | Unset = UNSET
    refinement_href: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        localized_aspect_value = self.localized_aspect_value

        match_count = self.match_count

        refinement_href = self.refinement_href

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if localized_aspect_value is not UNSET:
            field_dict["localizedAspectValue"] = localized_aspect_value
        if match_count is not UNSET:
            field_dict["matchCount"] = match_count
        if refinement_href is not UNSET:
            field_dict["refinementHref"] = refinement_href

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        localized_aspect_value = d.pop("localizedAspectValue", UNSET)

        match_count = d.pop("matchCount", UNSET)

        refinement_href = d.pop("refinementHref", UNSET)

        aspect_value_distribution = cls(
            localized_aspect_value=localized_aspect_value,
            match_count=match_count,
            refinement_href=refinement_href,
        )

        aspect_value_distribution.additional_properties = d
        return aspect_value_distribution

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
