import logging

from finman.application.base_use_case import UseCase
from finman.application.exceptions import (
    CategoryNotFoundError,
    TransactorNotFoundError,
)
from finman.application.uow import UoW
from finman.domain.entities import (
    Category,
    Transaction,
    TransactionType,
    Transactor,
)
from finman.domain.interfaces import TransactionsRepository
from finman.presentation.schemas import NewTransaction


log = logging.getLogger(__name__)


class RecordTransactionUC(UseCase[NewTransaction, int]):
    def __init__(self, uow: UoW, transactions_repo: TransactionsRepository):
        self.uow = uow
        self.transactions_repo = transactions_repo

    async def __call__(self, data: NewTransaction) -> int:
        """Receives a transaction to save, returns its identifier"""
        transactor = await self.validate_transactor(data.transactor)
        category = await self.validate_category(data.category)
        transaction_type = TransactionType[data.type.upper()]
        transaction = Transaction(
            date=data.date,
            type=transaction_type,
            transactor=transactor,
            category=category,
            amount=data.amount,
            currency=data.currency,
        )
        log.debug("Received new transaction: %s", repr(transaction))
        transaction_id = await self.transactions_repo.save(transaction)
        await self.uow.commit()
        return transaction_id

    async def validate_transactor(self, transactor_name: str) -> Transactor:
        transactors = await self.transactions_repo.get_transactors()
        for transactor in transactors:
            if transactor.name == transactor_name:
                return transactor
        raise TransactorNotFoundError(transactor_name)

    async def validate_category(self, category_name: str) -> Category:
        categories = await self.transactions_repo.get_categories()
        for category in categories:
            if category.name == category_name:
                if not category.parent:
                    log.warning("Got top level category %s", repr(category))
                return category
        raise CategoryNotFoundError(category_name)
