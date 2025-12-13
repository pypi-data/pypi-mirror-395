from enum import Enum


class MarketplaceSoftwareCatalogsListOItem(str, Enum):
    CREATED = "created"
    MODIFIED = "modified"
    NAME = "name"
    VALUE_0 = "-created"
    VALUE_1 = "-modified"
    VALUE_2 = "-name"
    VALUE_3 = "-version"
    VERSION = "version"

    def __str__(self) -> str:
        return str(self.value)
