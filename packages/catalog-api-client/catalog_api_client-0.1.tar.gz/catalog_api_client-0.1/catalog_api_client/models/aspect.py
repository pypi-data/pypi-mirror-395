from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="Aspect")


@_attrs_define
class Aspect:
    """This type contains the name and values of a category aspect.

    Attributes:
        localized_name (str | Unset): The localized name of this category aspect.
        localized_values (list[str] | Unset): A list of the localized values of this category aspect.
    """

    localized_name: str | Unset = UNSET
    localized_values: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        localized_name = self.localized_name

        localized_values: list[str] | Unset = UNSET
        if not isinstance(self.localized_values, Unset):
            localized_values = self.localized_values

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if localized_name is not UNSET:
            field_dict["localizedName"] = localized_name
        if localized_values is not UNSET:
            field_dict["localizedValues"] = localized_values

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        localized_name = d.pop("localizedName", UNSET)

        localized_values = cast(list[str], d.pop("localizedValues", UNSET))

        aspect = cls(
            localized_name=localized_name,
            localized_values=localized_values,
        )

        aspect.additional_properties = d
        return aspect

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
