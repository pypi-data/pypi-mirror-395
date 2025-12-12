from datetime import timezone, datetime
from typing import Optional

import pytest

from daomodel import DAOModel
from daomodel.dao import DAO
from daomodel.fields import utc_now, Identifier, CurrentTimestampField, AutoUpdatingTimestampField
from daomodel.testing import TestDAOFactory

ZERO_TIMESTAMP = datetime(1970, 1, 1)


class BasicModel(DAOModel, table=True):
    id: Identifier[int]


class TimestampsModel(DAOModel, table=True):
    id: Identifier[int]
    name: Optional[str]
    created_at: datetime = CurrentTimestampField
    updated_at: datetime = AutoUpdatingTimestampField


@pytest.fixture(name='timestamps_model_dao')
def timestamps_model_dao_fixture(daos: TestDAOFactory) -> DAO:
    return daos[TimestampsModel]


def test_utc_now():
    now = utc_now()
    assert isinstance(now, datetime)
    assert now.tzinfo is timezone.utc


def test_current_timestamp(timestamps_model_dao: DAO):
    timestamps_model_dao.create(1)
    entry = timestamps_model_dao.get(1)
    assert entry.created_at is not None
    assert entry.created_at > ZERO_TIMESTAMP


def test_auto_updating_timestamp(timestamps_model_dao: DAO):
    timestamps_model_dao.create(1)
    entry = timestamps_model_dao.get(1)
    updated_at = entry.updated_at
    assert updated_at is not None
    assert updated_at > ZERO_TIMESTAMP

    entry.name = 'Test'
    timestamps_model_dao.commit()
    assert entry.updated_at > updated_at
