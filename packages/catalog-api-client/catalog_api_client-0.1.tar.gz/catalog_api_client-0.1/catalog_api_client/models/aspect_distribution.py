from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.aspect_value_distribution import AspectValueDistribution


T = TypeVar("T", bound="AspectDistribution")


@_attrs_define
class AspectDistribution:
    """This type contains information about one category aspect that is associated with a specified category.

    Attributes:
        aspect_value_distributions (list[AspectValueDistribution] | Unset): Contains information about one or more
            values of the category aspect identified by <b>localizedAspectName</b>.
        localized_aspect_name (str | Unset): The localized name of an aspect that is associated with the category
            identified by <b>dominantCategoryId</b>.
    """

    aspect_value_distributions: list[AspectValueDistribution] | Unset = UNSET
    localized_aspect_name: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        aspect_value_distributions: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.aspect_value_distributions, Unset):
            aspect_value_distributions = []
            for aspect_value_distributions_item_data in self.aspect_value_distributions:
                aspect_value_distributions_item = aspect_value_distributions_item_data.to_dict()
                aspect_value_distributions.append(aspect_value_distributions_item)

        localized_aspect_name = self.localized_aspect_name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if aspect_value_distributions is not UNSET:
            field_dict["aspectValueDistributions"] = aspect_value_distributions
        if localized_aspect_name is not UNSET:
            field_dict["localizedAspectName"] = localized_aspect_name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.aspect_value_distribution import AspectValueDistribution

        d = dict(src_dict)
        _aspect_value_distributions = d.pop("aspectValueDistributions", UNSET)
        aspect_value_distributions: list[AspectValueDistribution] | Unset = UNSET
        if _aspect_value_distributions is not UNSET:
            aspect_value_distributions = []
            for aspect_value_distributions_item_data in _aspect_value_distributions:
                aspect_value_distributions_item = AspectValueDistribution.from_dict(
                    aspect_value_distributions_item_data
                )

                aspect_value_distributions.append(aspect_value_distributions_item)

        localized_aspect_name = d.pop("localizedAspectName", UNSET)

        aspect_distribution = cls(
            aspect_value_distributions=aspect_value_distributions,
            localized_aspect_name=localized_aspect_name,
        )

        aspect_distribution.additional_properties = d
        return aspect_distribution

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
