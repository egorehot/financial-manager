from abc import ABC, abstractmethod
from collections.abc import Sequence
from datetime import datetime

from finman.domain.entities import (
    Category, Transaction, TransactionType, Transactor,
)


class TransactionsRepository(ABC):
    @abstractmethod
    async def save(self, transaction: Transaction) -> int:
        raise NotImplementedError

    @abstractmethod
    async def get_transactions(
            self,
            date_from: datetime | None = None,
            date_to: datetime | None = None,
            type_: TransactionType | None = None,
            category: Category | None = None,
            transactor: Transactor | None = None,
    ) -> Sequence[Transaction]:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, transaction_id: int) -> Transaction:
        raise NotImplementedError

    @abstractmethod
    async def update(self, transaction: Transaction) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, transaction_id: int) -> None:
        raise NotImplementedError
