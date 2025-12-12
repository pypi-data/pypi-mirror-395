from typing import Any

import pytest
from sqlalchemy.exc import IntegrityError

from daomodel import names_of
from daomodel.testing import labeled_tests, TestDAOFactory
from tests.model_factory import create_test_model
from tests.test_fields import BasicModel
from tests.test_fields__inherited import get_test_cases


@labeled_tests(get_test_cases(exclude=('optional', 'uuid')))
def test_required(annotation: Any):
    model_type = create_test_model(annotation)
    with TestDAOFactory() as daos:
        dao = daos[model_type]
        entry = dao.create_with(id=1, insert=False)
        with pytest.raises(IntegrityError):
            dao.insert(entry)


@labeled_tests(get_test_cases('uuid', exclude='optional'))
def test_required__uuid(annotation: Any):
    model_type = create_test_model(annotation)
    with TestDAOFactory() as daos:
        dao = daos[model_type]
        dao.create_with(id=1)
        entry = dao.find(id=1).only()
        # Since UUID has a default value, we test that it is Required by attempting to set it to None
        entry.value = None
        with pytest.raises(IntegrityError):
            dao.upsert(entry)


@labeled_tests(get_test_cases('optional', exclude='uuid'))
def test_optional(annotation: Any):
    model_type = create_test_model(annotation)
    with TestDAOFactory() as daos:
        dao = daos[model_type]
        dao.create_with(id=1)
        entry = dao.find(id=1).only()
        assert entry.value is None


@labeled_tests(get_test_cases('optional', 'uuid'))
def test_optional__uuid(annotation: Any):
    model_type = create_test_model(annotation)
    with TestDAOFactory() as daos:
        dao = daos[model_type]
        dao.create_with(id=1)
        entry = dao.find(id=1).only()
        assert entry.value is not None
        # Since UUID has a default value, we test that it is Optional by setting it to None
        entry.value = None
        dao.upsert(entry)
        entry = dao.find(id=1).only()
        assert entry.value is None


def test_identifier():
    assert BasicModel.get_pk_names() == ['id']
    assert create_test_model(str).get_pk_names() == ['id']


@labeled_tests(get_test_cases('identifier'))
def test_identifier__continued(annotation: Any):
    assert create_test_model(annotation, field_name='id2').get_pk_names() == ['id', 'id2']


@labeled_tests(get_test_cases(exclude='unsearchable'))
def test_searchable(annotation: Any):
    assert names_of(create_test_model(annotation).get_searchable_properties()) == ['id', 'value']


@labeled_tests(get_test_cases('unsearchable'))
def test_unsearchable(annotation: Any):
    assert names_of(create_test_model(annotation).get_searchable_properties()) == ['id']
