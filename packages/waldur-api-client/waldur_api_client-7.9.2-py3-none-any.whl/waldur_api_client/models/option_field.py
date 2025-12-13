from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.option_field_type_enum import OptionFieldTypeEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.cascade_config import CascadeConfig
    from ..models.component_multiplier_config import ComponentMultiplierConfig


T = TypeVar("T", bound="OptionField")


@_attrs_define
class OptionField:
    """
    Attributes:
        type_ (OptionFieldTypeEnum):
        label (str):
        help_text (Union[Unset, str]):
        required (Union[Unset, bool]):  Default: False.
        choices (Union[Unset, list[str]]):
        default (Union[Unset, str]):
        min_ (Union[Unset, int]):
        max_ (Union[Unset, int]):
        cascade_config (Union[Unset, CascadeConfig]):
        component_multiplier_config (Union[Unset, ComponentMultiplierConfig]):
    """

    type_: OptionFieldTypeEnum
    label: str
    help_text: Union[Unset, str] = UNSET
    required: Union[Unset, bool] = False
    choices: Union[Unset, list[str]] = UNSET
    default: Union[Unset, str] = UNSET
    min_: Union[Unset, int] = UNSET
    max_: Union[Unset, int] = UNSET
    cascade_config: Union[Unset, "CascadeConfig"] = UNSET
    component_multiplier_config: Union[Unset, "ComponentMultiplierConfig"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_.value

        label = self.label

        help_text = self.help_text

        required = self.required

        choices: Union[Unset, list[str]] = UNSET
        if not isinstance(self.choices, Unset):
            choices = self.choices

        default = self.default

        min_ = self.min_

        max_ = self.max_

        cascade_config: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.cascade_config, Unset):
            cascade_config = self.cascade_config.to_dict()

        component_multiplier_config: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.component_multiplier_config, Unset):
            component_multiplier_config = self.component_multiplier_config.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type_,
                "label": label,
            }
        )
        if help_text is not UNSET:
            field_dict["help_text"] = help_text
        if required is not UNSET:
            field_dict["required"] = required
        if choices is not UNSET:
            field_dict["choices"] = choices
        if default is not UNSET:
            field_dict["default"] = default
        if min_ is not UNSET:
            field_dict["min"] = min_
        if max_ is not UNSET:
            field_dict["max"] = max_
        if cascade_config is not UNSET:
            field_dict["cascade_config"] = cascade_config
        if component_multiplier_config is not UNSET:
            field_dict["component_multiplier_config"] = component_multiplier_config

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.cascade_config import CascadeConfig
        from ..models.component_multiplier_config import ComponentMultiplierConfig

        d = dict(src_dict)
        type_ = OptionFieldTypeEnum(d.pop("type"))

        label = d.pop("label")

        help_text = d.pop("help_text", UNSET)

        required = d.pop("required", UNSET)

        choices = cast(list[str], d.pop("choices", UNSET))

        default = d.pop("default", UNSET)

        min_ = d.pop("min", UNSET)

        max_ = d.pop("max", UNSET)

        _cascade_config = d.pop("cascade_config", UNSET)
        cascade_config: Union[Unset, CascadeConfig]
        if isinstance(_cascade_config, Unset):
            cascade_config = UNSET
        else:
            cascade_config = CascadeConfig.from_dict(_cascade_config)

        _component_multiplier_config = d.pop("component_multiplier_config", UNSET)
        component_multiplier_config: Union[Unset, ComponentMultiplierConfig]
        if isinstance(_component_multiplier_config, Unset):
            component_multiplier_config = UNSET
        else:
            component_multiplier_config = ComponentMultiplierConfig.from_dict(_component_multiplier_config)

        option_field = cls(
            type_=type_,
            label=label,
            help_text=help_text,
            required=required,
            choices=choices,
            default=default,
            min_=min_,
            max_=max_,
            cascade_config=cascade_config,
            component_multiplier_config=component_multiplier_config,
        )

        option_field.additional_properties = d
        return option_field

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
