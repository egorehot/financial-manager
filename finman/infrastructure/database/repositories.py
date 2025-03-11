import logging
from collections.abc import Sequence
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from finman.domain.entities import (
    DEFAULT_TZ,
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


log = logging.getLogger(__name__)


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
        log.info("Saving to database transaction %r", transaction_orm)
        self.uow.add(transaction_orm)
        await self.uow.flush()
        return transaction_orm.id

    async def get_transactions(
            self,
            filters: TransactionsFilter,
    ) -> Sequence[RecordedTransaction]:
        query = select(Transaction).limit(filters.limit)
        if filters.date_from is not None:
            query = query.where(Transaction.date >= filters.date_from)
        if filters.date_to is not None:
            query = query.where(Transaction.date < filters.date_to)
        if filters.types is not None:
            query = query.where(Transaction.type.in_(filters.types))
        if filters.transactors is not None:
            transactor_ids = await self._get_transactor_ids_by_names(
                filters.transactors,
            )
            query = query.where(Transaction.transactor_id.in_(transactor_ids))
        if filters.categories is not None:
            categories_ids = await self._get_category_ids_by_names(
                filters.categories,
            )
            query = query.where(Transaction.category_id.in_(categories_ids))
        result = await self.uow.execute(query)
        transactions = result.scalars().all()
        return [RecordedTransaction.model_validate(t) for t in transactions]

    async def get_by_id(
            self, transaction_id: int,
    ) -> RecordedTransaction | None:
        log.info(
            "Getting transaction with id %s from database", transaction_id,
        )
        transaction = await self.uow.get(Transaction, transaction_id)
        if transaction is not None:
            log.info("Got transaction %r", transaction)
            return RecordedTransaction(
                id=transaction.id,
                date=datetime.fromtimestamp(transaction.date, tz=DEFAULT_TZ),
                amount=transaction.amount,
                currency=transaction.currency,  # type: ignore
                category=transaction.category.name,
                transactor=transaction.transactor.name,
                created_at=datetime.fromtimestamp(
                    transaction.created_at, tz=DEFAULT_TZ,
                ),
                updated_at=datetime.fromtimestamp(
                    transaction.updated_at, tz=DEFAULT_TZ,
                ),
                type=transaction.type,  # type: ignore
            )
        return None

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

    async def _get_transactor_ids_by_names(
            self, names: Sequence[str],
    ) -> Sequence[int]:
        query = select(Transactor.id).where(Transactor.name.in_(names))
        ids = await self.uow.execute(query)
        return ids.scalars().all()

    async def _get_category_ids_by_names(
            self, names: Sequence[str],
    ) -> Sequence[int]:
        query = select(Category.id).where(Category.name.in_(names))
        ids = await self.uow.execute(query)
        return ids.scalars().all()
