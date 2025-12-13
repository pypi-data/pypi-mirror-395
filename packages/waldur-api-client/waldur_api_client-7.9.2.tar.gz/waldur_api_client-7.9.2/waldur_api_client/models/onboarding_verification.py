import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.onboarding_verification_status_enum import OnboardingVerificationStatusEnum
from ..models.validation_method_enum import ValidationMethodEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.onboarding_verification_onboarding_metadata import OnboardingVerificationOnboardingMetadata
    from ..models.onboarding_verification_user_submitted_customer_data import (
        OnboardingVerificationUserSubmittedCustomerData,
    )


T = TypeVar("T", bound="OnboardingVerification")


@_attrs_define
class OnboardingVerification:
    """
    Attributes:
        uuid (UUID):
        user (int): User requesting company onboarding
        country (str): ISO country code (e.g., 'EE' for Estonia)
        status (OnboardingVerificationStatusEnum):
        validation_method (ValidationMethodEnum):
        verified_user_roles (Any): Roles the user has in the company
        verified_company_data (Any): Company information retrieved during validation
        raw_response (Any): Raw API response for debugging and auditing
        error_traceback (str):
        error_message (str):
        validated_at (Union[None, datetime.datetime]): When validation was completed
        customer (Union[None, int]): Customer created after successful validation
        onboarding_metadata (OnboardingVerificationOnboardingMetadata): Onboarding-specific data like intents, purposes
            extracted from checklist answers
        user_submitted_customer_data (OnboardingVerificationUserSubmittedCustomerData): Get customer data submitted by
            the user during onboarding.
        created (datetime.datetime):
        modified (datetime.datetime):
        legal_person_identifier (Union[Unset, str]): Official company registration code (required for automatic
            validation)
        legal_name (Union[Unset, str]): Company name(optional, for reference)
        expires_at (Union[None, Unset, datetime.datetime]): When this verification expires
    """

    uuid: UUID
    user: int
    country: str
    status: OnboardingVerificationStatusEnum
    validation_method: ValidationMethodEnum
    verified_user_roles: Any
    verified_company_data: Any
    raw_response: Any
    error_traceback: str
    error_message: str
    validated_at: Union[None, datetime.datetime]
    customer: Union[None, int]
    onboarding_metadata: "OnboardingVerificationOnboardingMetadata"
    user_submitted_customer_data: "OnboardingVerificationUserSubmittedCustomerData"
    created: datetime.datetime
    modified: datetime.datetime
    legal_person_identifier: Union[Unset, str] = UNSET
    legal_name: Union[Unset, str] = UNSET
    expires_at: Union[None, Unset, datetime.datetime] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        user = self.user

        country = self.country

        status = self.status.value

        validation_method = self.validation_method.value

        verified_user_roles = self.verified_user_roles

        verified_company_data = self.verified_company_data

        raw_response = self.raw_response

        error_traceback = self.error_traceback

        error_message = self.error_message

        validated_at: Union[None, str]
        if isinstance(self.validated_at, datetime.datetime):
            validated_at = self.validated_at.isoformat()
        else:
            validated_at = self.validated_at

        customer: Union[None, int]
        customer = self.customer

        onboarding_metadata = self.onboarding_metadata.to_dict()

        user_submitted_customer_data = self.user_submitted_customer_data.to_dict()

        created = self.created.isoformat()

        modified = self.modified.isoformat()

        legal_person_identifier = self.legal_person_identifier

        legal_name = self.legal_name

        expires_at: Union[None, Unset, str]
        if isinstance(self.expires_at, Unset):
            expires_at = UNSET
        elif isinstance(self.expires_at, datetime.datetime):
            expires_at = self.expires_at.isoformat()
        else:
            expires_at = self.expires_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "user": user,
                "country": country,
                "status": status,
                "validation_method": validation_method,
                "verified_user_roles": verified_user_roles,
                "verified_company_data": verified_company_data,
                "raw_response": raw_response,
                "error_traceback": error_traceback,
                "error_message": error_message,
                "validated_at": validated_at,
                "customer": customer,
                "onboarding_metadata": onboarding_metadata,
                "user_submitted_customer_data": user_submitted_customer_data,
                "created": created,
                "modified": modified,
            }
        )
        if legal_person_identifier is not UNSET:
            field_dict["legal_person_identifier"] = legal_person_identifier
        if legal_name is not UNSET:
            field_dict["legal_name"] = legal_name
        if expires_at is not UNSET:
            field_dict["expires_at"] = expires_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.onboarding_verification_onboarding_metadata import OnboardingVerificationOnboardingMetadata
        from ..models.onboarding_verification_user_submitted_customer_data import (
            OnboardingVerificationUserSubmittedCustomerData,
        )

        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        user = d.pop("user")

        country = d.pop("country")

        status = OnboardingVerificationStatusEnum(d.pop("status"))

        validation_method = ValidationMethodEnum(d.pop("validation_method"))

        verified_user_roles = d.pop("verified_user_roles")

        verified_company_data = d.pop("verified_company_data")

        raw_response = d.pop("raw_response")

        error_traceback = d.pop("error_traceback")

        error_message = d.pop("error_message")

        def _parse_validated_at(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                validated_at_type_0 = isoparse(data)

                return validated_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        validated_at = _parse_validated_at(d.pop("validated_at"))

        def _parse_customer(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        customer = _parse_customer(d.pop("customer"))

        onboarding_metadata = OnboardingVerificationOnboardingMetadata.from_dict(d.pop("onboarding_metadata"))

        user_submitted_customer_data = OnboardingVerificationUserSubmittedCustomerData.from_dict(
            d.pop("user_submitted_customer_data")
        )

        created = isoparse(d.pop("created"))

        modified = isoparse(d.pop("modified"))

        legal_person_identifier = d.pop("legal_person_identifier", UNSET)

        legal_name = d.pop("legal_name", UNSET)

        def _parse_expires_at(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                expires_at_type_0 = isoparse(data)

                return expires_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        expires_at = _parse_expires_at(d.pop("expires_at", UNSET))

        onboarding_verification = cls(
            uuid=uuid,
            user=user,
            country=country,
            status=status,
            validation_method=validation_method,
            verified_user_roles=verified_user_roles,
            verified_company_data=verified_company_data,
            raw_response=raw_response,
            error_traceback=error_traceback,
            error_message=error_message,
            validated_at=validated_at,
            customer=customer,
            onboarding_metadata=onboarding_metadata,
            user_submitted_customer_data=user_submitted_customer_data,
            created=created,
            modified=modified,
            legal_person_identifier=legal_person_identifier,
            legal_name=legal_name,
            expires_at=expires_at,
        )

        onboarding_verification.additional_properties = d
        return onboarding_verification

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
