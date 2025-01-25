import logging
from datetime import datetime

from finman.application.base_use_case import UseCase
from finman.application.dtos import TransactionResponse, TransactionsFilter
from finman.application.exceptions import IncorrectFilterDatesError
from finman.application.uow import UoW
from finman.application.utils import convert_transaction_to_response
from finman.domain.entities import (
    Category,
    TransactionType,
    Transactor,
)
from finman.domain.interfaces import TransactionsRepository


log = logging.getLogger(__name__)


class GetTransactions(
    UseCase[TransactionsFilter, list[TransactionResponse]],
):
    def __init__(self, uow: UoW, transactions_repo: TransactionsRepository):
        self.uow = uow
        self.transactions_repo = transactions_repo

    async def __call__(
            self, data: TransactionsFilter,
    ) -> list[TransactionResponse]:
        """Receives filters for transactions,
        returns list of transactions if found"""
        log.info("Getting transaction,list with filters: %s", repr(data))
        date_from, date_to = self.validate_dates(data.date_from, data.date_to)
        types = ([TransactionType[t.upper()] for t in data.types]
                 if data.types else None)
        categories = ([Category(name=c_name) for c_name in data.categories]
                      if data.categories else None)
        transactors = ([Transactor(name=t_name) for t_name in data.transactors]
                       if data.transactors else None)
        transactions = await self.transactions_repo.get_transactions(
            date_from=date_from,
            date_to=date_to,
            types=types,
            categories=categories,
            transactors=transactors,
            limit=data.limit,  # TODO add pagination
        )
        log.info("Got %s transactions", len(transactions))
        return [convert_transaction_to_response(transaction)
                for transaction in transactions]

    @staticmethod
    def validate_dates(
            date_from: datetime | None, date_to: datetime | None,
    ) -> tuple[datetime | None, datetime | None]:
        if (isinstance(date_from, datetime) and isinstance(date_to, datetime)
                and date_from > date_to):
            raise IncorrectFilterDatesError(date_from, date_to)
        return date_from, date_to


