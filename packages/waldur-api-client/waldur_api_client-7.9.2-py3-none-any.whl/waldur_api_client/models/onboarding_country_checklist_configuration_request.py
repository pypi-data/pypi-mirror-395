from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="OnboardingCountryChecklistConfigurationRequest")


@_attrs_define
class OnboardingCountryChecklistConfigurationRequest:
    """
    Attributes:
        country (str): ISO country code (e.g., 'EE' for Estonia)
        checklist (str): Checklist to use for this country's onboarding
        is_active (Union[Unset, bool]): Whether this country configuration is active
    """

    country: str
    checklist: str
    is_active: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        country = self.country

        checklist = self.checklist

        is_active = self.is_active

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "country": country,
                "checklist": checklist,
            }
        )
        if is_active is not UNSET:
            field_dict["is_active"] = is_active

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        country = d.pop("country")

        checklist = d.pop("checklist")

        is_active = d.pop("is_active", UNSET)

        onboarding_country_checklist_configuration_request = cls(
            country=country,
            checklist=checklist,
            is_active=is_active,
        )

        onboarding_country_checklist_configuration_request.additional_properties = d
        return onboarding_country_checklist_configuration_request

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
