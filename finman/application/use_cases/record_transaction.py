import logging

from finman.application.base_use_case import UseCase
from finman.application.exceptions import (
    CategoryNotFoundError,
    TransactorNotFoundError,
)
from finman.application.uow import UoW
from finman.domain.entities import NewTransaction
from finman.domain.interfaces import TransactionsRepository


log = logging.getLogger(__name__)


class RecordTransaction(UseCase[NewTransaction, int]):
    def __init__(self, uow: UoW, transactions_repo: TransactionsRepository):
        self.uow = uow
        self.transactions_repo = transactions_repo

    async def __call__(self, data: NewTransaction) -> int:
        """Receives a transaction to save, returns its identifier"""
        log.debug("Received new transaction: %s", repr(data))
        try:
            data.transactor = await self.validate_transactor(data.transactor)
            data.category = await self.validate_category(data.category)
            transaction_id = await self.transactions_repo.save(data)
            await self.uow.commit()
        except Exception as exc:
            await self.uow.rollback()
            log.exception(exc)
            raise
        else:
            return transaction_id

    async def validate_transactor(self, transactor_name: str) -> str:
        transactors = await self.transactions_repo.get_transactors()
        for transactor in transactors:
            if transactor == transactor_name.strip().lower().title():
                return transactor
        raise TransactorNotFoundError(transactor_name)

    async def validate_category(self, category_name: str) -> str:
        categories = await self.transactions_repo.get_categories()
        for category in categories:
            if category == category_name.strip().lower().title():
                return category
        raise CategoryNotFoundError(category_name)
