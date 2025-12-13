import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="SoftwareVersion")


@_attrs_define
class SoftwareVersion:
    """
    Attributes:
        url (str):
        uuid (UUID):
        created (datetime.datetime):
        modified (datetime.datetime):
        version (str):
        release_date (Union[None, datetime.date]):
        dependencies (Any): Package dependencies (format varies by catalog type)
        metadata (Any): Version-specific metadata (toolchains, build info, modules, etc.)
        package_name (str):
        catalog_type (str):
        target_count (int):
    """

    url: str
    uuid: UUID
    created: datetime.datetime
    modified: datetime.datetime
    version: str
    release_date: Union[None, datetime.date]
    dependencies: Any
    metadata: Any
    package_name: str
    catalog_type: str
    target_count: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        uuid = str(self.uuid)

        created = self.created.isoformat()

        modified = self.modified.isoformat()

        version = self.version

        release_date: Union[None, str]
        if isinstance(self.release_date, datetime.date):
            release_date = self.release_date.isoformat()
        else:
            release_date = self.release_date

        dependencies = self.dependencies

        metadata = self.metadata

        package_name = self.package_name

        catalog_type = self.catalog_type

        target_count = self.target_count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
                "uuid": uuid,
                "created": created,
                "modified": modified,
                "version": version,
                "release_date": release_date,
                "dependencies": dependencies,
                "metadata": metadata,
                "package_name": package_name,
                "catalog_type": catalog_type,
                "target_count": target_count,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        url = d.pop("url")

        uuid = UUID(d.pop("uuid"))

        created = isoparse(d.pop("created"))

        modified = isoparse(d.pop("modified"))

        version = d.pop("version")

        def _parse_release_date(data: object) -> Union[None, datetime.date]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                release_date_type_0 = isoparse(data).date()

                return release_date_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.date], data)

        release_date = _parse_release_date(d.pop("release_date"))

        dependencies = d.pop("dependencies")

        metadata = d.pop("metadata")

        package_name = d.pop("package_name")

        catalog_type = d.pop("catalog_type")

        target_count = d.pop("target_count")

        software_version = cls(
            url=url,
            uuid=uuid,
            created=created,
            modified=modified,
            version=version,
            release_date=release_date,
            dependencies=dependencies,
            metadata=metadata,
            package_name=package_name,
            catalog_type=catalog_type,
            target_count=target_count,
        )

        software_version.additional_properties = d
        return software_version

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
