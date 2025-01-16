from dataclasses import dataclass, fields, is_dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Literal, Optional


class TransactionType(Enum):
    EXPENSE = 1
    INCOME = 2


@dataclass
class Transaction:
    type: TransactionType
    date: datetime
    transactor: "Transactor"
    category: "Category"
    amount: float
    currency: "Currency"

    @classmethod
    def from_object(cls, data: Any) -> "Transaction":
        kwargs = {}
        for field in fields(cls):
            value = getattr(data, field.name, None)
            if is_dataclass(field.type):
                value = field.type(name=value)
            elif isinstance(field.type, type) and issubclass(field.type, Enum):
                value = field.type[value.upper()]
            kwargs[field.name] = value
        return cls(**kwargs)


@dataclass
class Transactor:
    name: str


@dataclass
class Category:
    name: str
    parent: Optional["Category"] = None


@dataclass
class Currency:
    name: Literal["USD", "EUR", "RUB"]
