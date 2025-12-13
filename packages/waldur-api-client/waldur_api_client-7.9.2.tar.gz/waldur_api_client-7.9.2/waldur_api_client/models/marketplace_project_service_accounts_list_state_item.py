from enum import Enum


class MarketplaceProjectServiceAccountsListStateItem(str, Enum):
    CLOSED = "Closed"
    ERRED = "Erred"
    OK = "OK"

    def __str__(self) -> str:
        return str(self.value)
