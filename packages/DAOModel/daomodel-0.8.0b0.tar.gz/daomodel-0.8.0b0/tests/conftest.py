from typing import Any, Generator

import pytest

from daomodel.testing import TestDAOFactory


@pytest.fixture(name='daos')
def daos_fixture() -> Generator[TestDAOFactory, Any, None]:
    """
    Provides a DAOFactory for Testing as a pytest fixture named `daos`.
    """
    with TestDAOFactory() as daos:
        yield daos
