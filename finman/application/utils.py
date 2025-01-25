from finman.application.dtos import TransactionResponse
from finman.domain.entities import Transaction


def convert_transaction_to_response(
        transaction: Transaction,
) -> TransactionResponse:
    data = transaction.model_dump(mode="json")
    data["transactor"] = data["transactor"].get("name")
    data["category"] = data["category"].get("name")
    return TransactionResponse(**data)
