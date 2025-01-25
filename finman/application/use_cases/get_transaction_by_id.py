from finman.application.base_use_case import UseCase
from finman.application.dtos import TransactionResponse
from finman.application.uow import UoW
from finman.application.utils import convert_transaction_to_response
from finman.domain.interfaces import TransactionsRepository


class GetTransactionById(UseCase[int, TransactionResponse | None]):
    def __init__(self, uow: UoW, transactions_repo: TransactionsRepository):
        self.uow = uow
        self.transactions_repo = transactions_repo

    async def __call__(self, data: int) -> TransactionResponse | None:
        transaction = await self.transactions_repo.get_by_id(data)
        if transaction:
            return convert_transaction_to_response(transaction)
        return None
