import pytest

from finman.infrastructure.database.models import Category, Transactor
from finman.infrastructure.database.repositories import (
    SQLAlchemyTransactionsRepository,
)


@pytest.fixture(scope="module")
async def aux_data(sessionmaker):
    async with sessionmaker() as session:
        session.add(Category(name="Test Category"))
        session.add(Transactor(name="Test Transactor"))
        await session.commit()


@pytest.fixture
async def repository(sessionmaker, aux_data):
    async with sessionmaker() as session:
        yield SQLAlchemyTransactionsRepository(session)
