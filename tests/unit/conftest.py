from unittest.mock import Mock

import pytest

from finman.application.uow import UoW
from finman.domain.interfaces import TransactionsRepository


@pytest.fixture
def uow():
    return Mock(spec=UoW)


@pytest.fixture
def transactions_repo():
    return Mock(spec=TransactionsRepository)
