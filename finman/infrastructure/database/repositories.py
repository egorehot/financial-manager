from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from finman.domain.entities import (
    NewTransaction,
    RecordedTransaction,
    TransactionsFilter,
)
from finman.domain.exceptions import (
    CategoryNotFoundError,
    TransactorNotFoundError,
)
from finman.domain.interfaces import TransactionsRepository
from finman.infrastructure.database.models import (
    Category,
    Transaction,
    Transactor,
)


class SQLAlchemyTransactionsRepository(TransactionsRepository):
    def __init__(self, uow: AsyncSession):
        self.uow = uow

    async def save(self, transaction: NewTransaction) -> int:
        category = await self._get_category(transaction.category)
        transactor = await self._get_transactor(transaction.transactor)
        transaction_orm = Transaction(
            date=int(transaction.date.timestamp()),
            amount=transaction.amount,
            currency=transaction.currency,
            type=transaction.type.value,
            category=category,
            transactor=transactor,
        )
        self.uow.add(transaction_orm)
        await self.uow.flush()
        return transaction_orm.id

    async def get_transactions(
            self,
            filters: TransactionsFilter,
    ) -> Sequence[RecordedTransaction]:
        pass  # TODO

    async def get_by_id(self, transaction_id: int) -> RecordedTransaction:
        pass  # TODO

    async def update(
            self,
            transaction_id: int,
            transaction: NewTransaction,
    ) -> None:
        pass  # TODO

    async def delete(self, transaction_id: int) -> None:
        pass  # TODO

    async def _get_category(self, name: str) -> Category:
        result = await self.uow.execute(select(Category).filter_by(name=name))
        category = result.scalar_one_or_none()
        if category is None:
            raise CategoryNotFoundError(name)
        return category

    async def _get_transactor(self, name: str) -> Transactor:
        result = await self.uow.execute(
            select(Transactor).filter_by(name=name),
        )
        transactor = result.scalar_one_or_none()
        if transactor is None:
            raise TransactorNotFoundError(name)
        return transactor
