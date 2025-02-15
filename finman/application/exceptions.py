class TransactionNotFoundError(ValueError):
    def __init__(self, transaction_id: int):
        super().__init__(f"Transaction with id={transaction_id!s} not found")
