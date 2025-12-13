from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="OnboardingCompanyValidationRequestRequest")


@_attrs_define
class OnboardingCompanyValidationRequestRequest:
    """
    Attributes:
        country (str): ISO country code (e.g., 'EE' for Estonia)
        legal_person_identifier (Union[Unset, str]): Official company registration code
        legal_name (Union[Unset, str]): Company name (optional)
        is_manual_validation (Union[Unset, bool]): Indicates if the validation is to be performed manually Default:
            False.
    """

    country: str
    legal_person_identifier: Union[Unset, str] = UNSET
    legal_name: Union[Unset, str] = UNSET
    is_manual_validation: Union[Unset, bool] = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        country = self.country

        legal_person_identifier = self.legal_person_identifier

        legal_name = self.legal_name

        is_manual_validation = self.is_manual_validation

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "country": country,
            }
        )
        if legal_person_identifier is not UNSET:
            field_dict["legal_person_identifier"] = legal_person_identifier
        if legal_name is not UNSET:
            field_dict["legal_name"] = legal_name
        if is_manual_validation is not UNSET:
            field_dict["is_manual_validation"] = is_manual_validation

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        country = d.pop("country")

        legal_person_identifier = d.pop("legal_person_identifier", UNSET)

        legal_name = d.pop("legal_name", UNSET)

        is_manual_validation = d.pop("is_manual_validation", UNSET)

        onboarding_company_validation_request_request = cls(
            country=country,
            legal_person_identifier=legal_person_identifier,
            legal_name=legal_name,
            is_manual_validation=is_manual_validation,
        )

        onboarding_company_validation_request_request.additional_properties = d
        return onboarding_company_validation_request_request

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
