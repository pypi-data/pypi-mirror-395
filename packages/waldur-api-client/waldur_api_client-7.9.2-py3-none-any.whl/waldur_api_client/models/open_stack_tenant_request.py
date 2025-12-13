from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.open_stack_tenant_security_group_request import OpenStackTenantSecurityGroupRequest


T = TypeVar("T", bound="OpenStackTenantRequest")


@_attrs_define
class OpenStackTenantRequest:
    """
    Attributes:
        name (str):
        service_settings (str):
        project (str):
        description (Union[Unset, str]):
        availability_zone (Union[Unset, str]): Optional availability group. Will be used for all instances provisioned
            in this tenant
        user_username (Union[Unset, str]): Username of the tenant user
        user_password (Union[Unset, str]): Password of the tenant user
        subnet_cidr (Union[Unset, str]):  Default: '192.168.42.0/24'.
        default_volume_type_name (Union[Unset, str]): Volume type name to use when creating volumes.
        security_groups (Union[Unset, list['OpenStackTenantSecurityGroupRequest']]):
    """

    name: str
    service_settings: str
    project: str
    description: Union[Unset, str] = UNSET
    availability_zone: Union[Unset, str] = UNSET
    user_username: Union[Unset, str] = UNSET
    user_password: Union[Unset, str] = UNSET
    subnet_cidr: Union[Unset, str] = "192.168.42.0/24"
    default_volume_type_name: Union[Unset, str] = UNSET
    security_groups: Union[Unset, list["OpenStackTenantSecurityGroupRequest"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        service_settings = self.service_settings

        project = self.project

        description = self.description

        availability_zone = self.availability_zone

        user_username = self.user_username

        user_password = self.user_password

        subnet_cidr = self.subnet_cidr

        default_volume_type_name = self.default_volume_type_name

        security_groups: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.security_groups, Unset):
            security_groups = []
            for security_groups_item_data in self.security_groups:
                security_groups_item = security_groups_item_data.to_dict()
                security_groups.append(security_groups_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "service_settings": service_settings,
                "project": project,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if availability_zone is not UNSET:
            field_dict["availability_zone"] = availability_zone
        if user_username is not UNSET:
            field_dict["user_username"] = user_username
        if user_password is not UNSET:
            field_dict["user_password"] = user_password
        if subnet_cidr is not UNSET:
            field_dict["subnet_cidr"] = subnet_cidr
        if default_volume_type_name is not UNSET:
            field_dict["default_volume_type_name"] = default_volume_type_name
        if security_groups is not UNSET:
            field_dict["security_groups"] = security_groups

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.open_stack_tenant_security_group_request import OpenStackTenantSecurityGroupRequest

        d = dict(src_dict)
        name = d.pop("name")

        service_settings = d.pop("service_settings")

        project = d.pop("project")

        description = d.pop("description", UNSET)

        availability_zone = d.pop("availability_zone", UNSET)

        user_username = d.pop("user_username", UNSET)

        user_password = d.pop("user_password", UNSET)

        subnet_cidr = d.pop("subnet_cidr", UNSET)

        default_volume_type_name = d.pop("default_volume_type_name", UNSET)

        security_groups = []
        _security_groups = d.pop("security_groups", UNSET)
        for security_groups_item_data in _security_groups or []:
            security_groups_item = OpenStackTenantSecurityGroupRequest.from_dict(security_groups_item_data)

            security_groups.append(security_groups_item)

        open_stack_tenant_request = cls(
            name=name,
            service_settings=service_settings,
            project=project,
            description=description,
            availability_zone=availability_zone,
            user_username=user_username,
            user_password=user_password,
            subnet_cidr=subnet_cidr,
            default_volume_type_name=default_volume_type_name,
            security_groups=security_groups,
        )

        open_stack_tenant_request.additional_properties = d
        return open_stack_tenant_request

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
