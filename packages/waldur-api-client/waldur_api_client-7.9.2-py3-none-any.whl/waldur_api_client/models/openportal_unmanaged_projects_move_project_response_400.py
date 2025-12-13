from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="OpenportalUnmanagedProjectsMoveProjectResponse400")


@_attrs_define
class OpenportalUnmanagedProjectsMoveProjectResponse400:
    """Validation error when trying to move a terminated project

    Example:
        {'non_field_errors': ['Cannot move terminated projects.']}

    Attributes:
        non_field_errors (Union[Unset, list[str]]):
    """

    non_field_errors: Union[Unset, list[str]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        non_field_errors: Union[Unset, list[str]] = UNSET
        if not isinstance(self.non_field_errors, Unset):
            non_field_errors = self.non_field_errors

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if non_field_errors is not UNSET:
            field_dict["non_field_errors"] = non_field_errors

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        non_field_errors = cast(list[str], d.pop("non_field_errors", UNSET))

        openportal_unmanaged_projects_move_project_response_400 = cls(
            non_field_errors=non_field_errors,
        )

        openportal_unmanaged_projects_move_project_response_400.additional_properties = d
        return openportal_unmanaged_projects_move_project_response_400

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
