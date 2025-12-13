from enum import Enum


class MarketplaceSoftwareTargetsCountOItem(str, Enum):
    CPU_FAMILY = "cpu_family"
    CPU_MICROARCHITECTURE = "cpu_microarchitecture"
    CREATED = "created"
    PACKAGE_NAME = "package_name"
    VALUE_0 = "-cpu_family"
    VALUE_1 = "-cpu_microarchitecture"
    VALUE_2 = "-created"
    VALUE_3 = "-package_name"

    def __str__(self) -> str:
        return str(self.value)
