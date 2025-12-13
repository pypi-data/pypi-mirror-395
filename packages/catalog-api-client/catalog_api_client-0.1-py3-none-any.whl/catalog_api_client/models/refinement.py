from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.aspect_distribution import AspectDistribution


T = TypeVar("T", bound="Refinement")


@_attrs_define
class Refinement:
    """This type identifies a product category and the aspects associated with that category. Each aspect distribution
    container returns the distribution of values that have been used for the aspect.

        Attributes:
            aspect_distributions (list[AspectDistribution] | Unset): Contains information about one or more aspects that are
                associated with the category identified by <b>dominantCategoryId</b>.
            dominant_category_id (str | Unset): The ID of the category that eBay determines is most likely to cover the
                products matching the search criteria.
    """

    aspect_distributions: list[AspectDistribution] | Unset = UNSET
    dominant_category_id: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        aspect_distributions: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.aspect_distributions, Unset):
            aspect_distributions = []
            for aspect_distributions_item_data in self.aspect_distributions:
                aspect_distributions_item = aspect_distributions_item_data.to_dict()
                aspect_distributions.append(aspect_distributions_item)

        dominant_category_id = self.dominant_category_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if aspect_distributions is not UNSET:
            field_dict["aspectDistributions"] = aspect_distributions
        if dominant_category_id is not UNSET:
            field_dict["dominantCategoryId"] = dominant_category_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.aspect_distribution import AspectDistribution

        d = dict(src_dict)
        _aspect_distributions = d.pop("aspectDistributions", UNSET)
        aspect_distributions: list[AspectDistribution] | Unset = UNSET
        if _aspect_distributions is not UNSET:
            aspect_distributions = []
            for aspect_distributions_item_data in _aspect_distributions:
                aspect_distributions_item = AspectDistribution.from_dict(aspect_distributions_item_data)

                aspect_distributions.append(aspect_distributions_item)

        dominant_category_id = d.pop("dominantCategoryId", UNSET)

        refinement = cls(
            aspect_distributions=aspect_distributions,
            dominant_category_id=dominant_category_id,
        )

        refinement.additional_properties = d
        return refinement

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
