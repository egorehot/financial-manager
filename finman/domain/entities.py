from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Literal


class TransactionType(Enum):
    EXPENSE = 1
    INCOME = 2


@dataclass
class Transaction:
    type_: TransactionType
    date: datetime
    transactor: "User"
    category: "Category"
    amount: float
    currency: "Currency"


@dataclass
class User:
    name: str


@dataclass
class Category:
    name: str
    parent: "Category"


@dataclass
class Currency:
    name: Literal["USD", "EUR", "RUB"]
