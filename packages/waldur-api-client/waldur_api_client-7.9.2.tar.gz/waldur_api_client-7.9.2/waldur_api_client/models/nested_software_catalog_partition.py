from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="NestedSoftwareCatalogPartition")


@_attrs_define
class NestedSoftwareCatalogPartition:
    """
    Attributes:
        uuid (Union[Unset, str]):
        partition_name (Union[Unset, str]):
        priority_tier (Union[Unset, int]):
        qos (Union[Unset, str]):
    """

    uuid: Union[Unset, str] = UNSET
    partition_name: Union[Unset, str] = UNSET
    priority_tier: Union[Unset, int] = UNSET
    qos: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = self.uuid

        partition_name = self.partition_name

        priority_tier = self.priority_tier

        qos = self.qos

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if uuid is not UNSET:
            field_dict["uuid"] = uuid
        if partition_name is not UNSET:
            field_dict["partition_name"] = partition_name
        if priority_tier is not UNSET:
            field_dict["priority_tier"] = priority_tier
        if qos is not UNSET:
            field_dict["qos"] = qos

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = d.pop("uuid", UNSET)

        partition_name = d.pop("partition_name", UNSET)

        priority_tier = d.pop("priority_tier", UNSET)

        qos = d.pop("qos", UNSET)

        nested_software_catalog_partition = cls(
            uuid=uuid,
            partition_name=partition_name,
            priority_tier=priority_tier,
            qos=qos,
        )

        nested_software_catalog_partition.additional_properties = d
        return nested_software_catalog_partition

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
