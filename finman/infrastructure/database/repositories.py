import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from finman.domain.entities import NewTransaction
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
        category_result = await self.uow.execute(
            sa.select(Category).filter_by(name=transaction.category),
        )
        category = category_result.scalar_one()
        transactor_result = await self.uow.execute(
            sa.select(Transactor).filter_by(name=transaction.transactor),
        )
        transactor = transactor_result.scalar_one()
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
        return transaction_orm.id  # TODO test
