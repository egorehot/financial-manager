from abc import ABC, abstractmethod
from collections.abc import Sequence
from datetime import datetime

from finman.domain.entities import (
    Category,
    Transaction,
    TransactionType,
    Transactor,
)


class TransactionsRepository(ABC):
    @abstractmethod
    async def save(self, transaction: Transaction) -> int:
        raise NotImplementedError

    @abstractmethod
    async def get_transactions(  # noqa: PLR0913
            self,
            date_from: datetime | None = None,
            date_to: datetime | None = None,
            types: list[TransactionType] | None = None,
            categories: list[Category] | None = None,
            transactors: list[Transactor] | None = None,
            limit: int = 100,
    ) -> Sequence[Transaction | None]:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, transaction_id: int) -> Transaction | None:
        raise NotImplementedError

    @abstractmethod
    async def update(self, transaction: Transaction) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, transaction_id: int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_transactors(self) -> Sequence[Transactor]:
        raise NotImplementedError

    @abstractmethod
    async def get_categories(self) -> Sequence[Category]:
        raise NotImplementedError
