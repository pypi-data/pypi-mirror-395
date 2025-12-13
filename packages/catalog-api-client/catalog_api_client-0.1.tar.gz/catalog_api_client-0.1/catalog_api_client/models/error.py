from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.error_parameter import ErrorParameter


T = TypeVar("T", bound="Error")


@_attrs_define
class Error:
    """This type defines the fields that can be returned in an error.

    Attributes:
        category (str | Unset): Identifies the type of erro.
        domain (str | Unset): Name for the primary system where the error occurred. This is relevant for application
            errors.
        error_id (int | Unset): A unique number to identify the error.
        input_ref_ids (list[str] | Unset): An array of request elements most closely associated to the error.
        long_message (str | Unset): A more detailed explanation of the error.
        message (str | Unset): Information on how to correct the problem, in the end user's terms and language where
            applicable.
        output_ref_ids (list[str] | Unset): An array of request elements most closely associated to the error.
        parameters (list[ErrorParameter] | Unset): An array of name/value pairs that describe details the error
            condition. These are useful when multiple errors are returned.
        subdomain (str | Unset): Further helps indicate which subsystem the error is coming from. System subcategories
            include: Initialization, Serialization, Security, Monitoring, Rate Limiting, etc.
    """

    category: str | Unset = UNSET
    domain: str | Unset = UNSET
    error_id: int | Unset = UNSET
    input_ref_ids: list[str] | Unset = UNSET
    long_message: str | Unset = UNSET
    message: str | Unset = UNSET
    output_ref_ids: list[str] | Unset = UNSET
    parameters: list[ErrorParameter] | Unset = UNSET
    subdomain: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        category = self.category

        domain = self.domain

        error_id = self.error_id

        input_ref_ids: list[str] | Unset = UNSET
        if not isinstance(self.input_ref_ids, Unset):
            input_ref_ids = self.input_ref_ids

        long_message = self.long_message

        message = self.message

        output_ref_ids: list[str] | Unset = UNSET
        if not isinstance(self.output_ref_ids, Unset):
            output_ref_ids = self.output_ref_ids

        parameters: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.parameters, Unset):
            parameters = []
            for parameters_item_data in self.parameters:
                parameters_item = parameters_item_data.to_dict()
                parameters.append(parameters_item)

        subdomain = self.subdomain

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if category is not UNSET:
            field_dict["category"] = category
        if domain is not UNSET:
            field_dict["domain"] = domain
        if error_id is not UNSET:
            field_dict["errorId"] = error_id
        if input_ref_ids is not UNSET:
            field_dict["inputRefIds"] = input_ref_ids
        if long_message is not UNSET:
            field_dict["longMessage"] = long_message
        if message is not UNSET:
            field_dict["message"] = message
        if output_ref_ids is not UNSET:
            field_dict["outputRefIds"] = output_ref_ids
        if parameters is not UNSET:
            field_dict["parameters"] = parameters
        if subdomain is not UNSET:
            field_dict["subdomain"] = subdomain

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.error_parameter import ErrorParameter

        d = dict(src_dict)
        category = d.pop("category", UNSET)

        domain = d.pop("domain", UNSET)

        error_id = d.pop("errorId", UNSET)

        input_ref_ids = cast(list[str], d.pop("inputRefIds", UNSET))

        long_message = d.pop("longMessage", UNSET)

        message = d.pop("message", UNSET)

        output_ref_ids = cast(list[str], d.pop("outputRefIds", UNSET))

        _parameters = d.pop("parameters", UNSET)
        parameters: list[ErrorParameter] | Unset = UNSET
        if _parameters is not UNSET:
            parameters = []
            for parameters_item_data in _parameters:
                parameters_item = ErrorParameter.from_dict(parameters_item_data)

                parameters.append(parameters_item)

        subdomain = d.pop("subdomain", UNSET)

        error = cls(
            category=category,
            domain=domain,
            error_id=error_id,
            input_ref_ids=input_ref_ids,
            long_message=long_message,
            message=message,
            output_ref_ids=output_ref_ids,
            parameters=parameters,
            subdomain=subdomain,
        )

        error.additional_properties = d
        return error

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
