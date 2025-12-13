from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.nested_software_catalog_catalog import NestedSoftwareCatalogCatalog
    from ..models.nested_software_catalog_partition import NestedSoftwareCatalogPartition


T = TypeVar("T", bound="NestedSoftwareCatalog")


@_attrs_define
class NestedSoftwareCatalog:
    """
    Attributes:
        uuid (Union[Unset, UUID]):
        catalog (Union[Unset, NestedSoftwareCatalogCatalog]):
        enabled_cpu_family (Union[Unset, Any]): List of enabled CPU families: ['x86_64', 'aarch64']
        enabled_cpu_microarchitectures (Union[Unset, Any]): List of enabled CPU microarchitectures: ['generic', 'zen3']
        package_count (Union[Unset, int]):
        partition (Union[Unset, NestedSoftwareCatalogPartition]):
    """

    uuid: Union[Unset, UUID] = UNSET
    catalog: Union[Unset, "NestedSoftwareCatalogCatalog"] = UNSET
    enabled_cpu_family: Union[Unset, Any] = UNSET
    enabled_cpu_microarchitectures: Union[Unset, Any] = UNSET
    package_count: Union[Unset, int] = UNSET
    partition: Union[Unset, "NestedSoftwareCatalogPartition"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid: Union[Unset, str] = UNSET
        if not isinstance(self.uuid, Unset):
            uuid = str(self.uuid)

        catalog: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.catalog, Unset):
            catalog = self.catalog.to_dict()

        enabled_cpu_family = self.enabled_cpu_family

        enabled_cpu_microarchitectures = self.enabled_cpu_microarchitectures

        package_count = self.package_count

        partition: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.partition, Unset):
            partition = self.partition.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if uuid is not UNSET:
            field_dict["uuid"] = uuid
        if catalog is not UNSET:
            field_dict["catalog"] = catalog
        if enabled_cpu_family is not UNSET:
            field_dict["enabled_cpu_family"] = enabled_cpu_family
        if enabled_cpu_microarchitectures is not UNSET:
            field_dict["enabled_cpu_microarchitectures"] = enabled_cpu_microarchitectures
        if package_count is not UNSET:
            field_dict["package_count"] = package_count
        if partition is not UNSET:
            field_dict["partition"] = partition

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.nested_software_catalog_catalog import NestedSoftwareCatalogCatalog
        from ..models.nested_software_catalog_partition import NestedSoftwareCatalogPartition

        d = dict(src_dict)
        _uuid = d.pop("uuid", UNSET)
        uuid: Union[Unset, UUID]
        if isinstance(_uuid, Unset):
            uuid = UNSET
        else:
            uuid = UUID(_uuid)

        _catalog = d.pop("catalog", UNSET)
        catalog: Union[Unset, NestedSoftwareCatalogCatalog]
        if isinstance(_catalog, Unset):
            catalog = UNSET
        else:
            catalog = NestedSoftwareCatalogCatalog.from_dict(_catalog)

        enabled_cpu_family = d.pop("enabled_cpu_family", UNSET)

        enabled_cpu_microarchitectures = d.pop("enabled_cpu_microarchitectures", UNSET)

        package_count = d.pop("package_count", UNSET)

        _partition = d.pop("partition", UNSET)
        partition: Union[Unset, NestedSoftwareCatalogPartition]
        if isinstance(_partition, Unset):
            partition = UNSET
        else:
            partition = NestedSoftwareCatalogPartition.from_dict(_partition)

        nested_software_catalog = cls(
            uuid=uuid,
            catalog=catalog,
            enabled_cpu_family=enabled_cpu_family,
            enabled_cpu_microarchitectures=enabled_cpu_microarchitectures,
            package_count=package_count,
            partition=partition,
        )

        nested_software_catalog.additional_properties = d
        return nested_software_catalog

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
