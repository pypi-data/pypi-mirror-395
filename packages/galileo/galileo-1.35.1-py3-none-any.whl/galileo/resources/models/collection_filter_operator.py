from enum import Enum


class CollectionFilterOperator(str, Enum):
    CONTAINS = "contains"
    EQ = "eq"
    NOT_IN = "not_in"

    def __str__(self) -> str:
        return str(self.value)
