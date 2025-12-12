from dataclasses import dataclass
from enum import Enum


class AuditOperator(Enum):
    EQUAL = "eq"
    GREATER_EQUAL = "gte"
    LESSER_EQUAL = "lte"
    LIKE = "like"


@dataclass
class AuditFilter:
    """
    Dataclass that models audit filters
    Attributes:
        field_name (str): name of the filter
        operator (AuditOperator): the filter operator
        value (str): the filter value
    """
    field_name: str
    operator: AuditOperator
    value: str

    def __post_init__(self):
        if self.field_name == '' or self.operator == '' or self.value == '':
            raise ValueError(f'{self.field_name} {self.operator} {self.value} cannot be empty')
        # Validate role
        if not isinstance(self.operator, AuditOperator):
            raise ValueError(f"Role must be one of {list(AuditOperator)}")
