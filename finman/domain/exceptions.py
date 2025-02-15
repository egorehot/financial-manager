from datetime import datetime


class DomainError(Exception):
    pass


class CategoryNotFoundError(DomainError):
    def __init__(self, category_name: str):
        super().__init__(f"Category '{category_name}' not found")


class TransactorNotFoundError(DomainError):
    def __init__(self, transactor_name: str):
        super().__init__(f"Transactor '{transactor_name!s}' not found")


class IncorrectFilterDatesError(ValueError):
    def __init__(self, date_from: datetime, date_to: datetime):
        super().__init__(f"Expected `date_from` <= `date_to`. "
                         f"Got {date_from=}, {date_to=}")
