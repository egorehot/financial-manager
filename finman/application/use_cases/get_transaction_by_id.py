from finman.application.base_use_case import UseCase
from finman.application.exceptions import TransactionNotFoundError
from finman.application.uow import UoW
from finman.domain.entities import TransactionResponse
from finman.domain.interfaces import TransactionsRepository


class GetTransactionById(UseCase[int, TransactionResponse]):
    def __init__(self, uow: UoW, transactions_repo: TransactionsRepository):
        self.uow = uow
        self.transactions_repo = transactions_repo

    async def __call__(self, data: int) -> TransactionResponse:
        transaction = await self.transactions_repo.get_by_id(data)
        if not transaction:
            raise TransactionNotFoundError(data)
        return transaction
