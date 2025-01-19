class TransactorNotFoundError(ValueError):
    def __init__(self, transactor_name: str):
        super().__init__(f"Transactor '{transactor_name!s}' not found")


class CategoryNotFoundError(ValueError):
    def __init__(self, category_name: str):
        super().__init__(f"Category '{category_name}' not found")
