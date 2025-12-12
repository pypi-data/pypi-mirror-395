from typing import Optional, Any
from uuid import UUID

from daomodel import DAOModel
from daomodel.fields import Identifier
from daomodel.testing import labeled_tests, TestDAOFactory
from tests.model_factory import create_test_model
from tests.test_fields import BasicModel
from tests.test_fields__inherited import get_test_cases


class OtherModel(DAOModel, table=True):
    id: Identifier[str]


class UUIDModel(DAOModel, table=True):
    id: Identifier[UUID]


class UUIDReferenceModel(DAOModel, table=True):
    id: Identifier[int]
    other_id: UUIDModel


class UUIDOptionalReferenceModel(DAOModel, table=True):
    id: Identifier[int]
    other_id: Optional[UUIDModel]


@labeled_tests({**get_test_cases('field')})
def test_field(annotation: Any):
    model_type = create_test_model(annotation)
    with TestDAOFactory() as daos:
        dao = daos[model_type]
        dao.create_with(id=1, value='test')
        entry = dao.find(id=1)
        assert entry.only().value == 'test'


@labeled_tests(get_test_cases('uuid'))
def test_uuid(annotation: Any):
    model_type = create_test_model(annotation)
    with TestDAOFactory() as daos:
        dao = daos[model_type]
        entry = dao.create_with(id=1)

        assert getattr(entry, 'value') is not None
        assert isinstance(getattr(entry, 'value'), UUID)

        entry2 = dao.create_with(id=2)
        assert getattr(entry2, 'value') is not None
        assert isinstance(getattr(entry2, 'value'), UUID)
        assert getattr(entry, 'value') != getattr(entry2, 'value')


@labeled_tests(get_test_cases('dict'))
def test_dict(annotation: Any):
    model_type = create_test_model(annotation)
    sample_dict = {'Hello': 'World!', 'Lorem': ['Ipsum', 'Dolor', 'Sit', 'Amet']}
    with TestDAOFactory() as daos:
        daos[model_type].create_with(id=1, value=sample_dict)
        daos.assert_in_db(model_type, 1, value=sample_dict)


@labeled_tests(get_test_cases('reference'))
def test_reference(annotation: Any):
    model_type = create_test_model(annotation)
    with TestDAOFactory() as daos:
        daos[BasicModel].create(100)
        dao = daos[model_type]
        dao.create_with(id=1, value=100)
        entry = dao.find(id=1)
        assert entry.only().value == 100


def test_reference__uuid(daos: TestDAOFactory):
    uuid_dao = daos[UUIDModel]
    reference_dao = daos[UUIDReferenceModel]

    uuid_model = daos[UUIDModel].create_with()
    reference_dao.create_with(id=1, other_id=uuid_model.id)

    entry = reference_dao.get(1)
    assert entry.other_id is not None
    assert uuid_dao.get(entry.other_id) is not None


def test_reference__uuid__optional(daos: TestDAOFactory):
    daos[UUIDOptionalReferenceModel].create(1)
    daos.assert_in_db(UUIDOptionalReferenceModel, 1, other_id=None)


@labeled_tests(get_test_cases('no_case_str', exclude='unsearchable'))
def test_no_case_str(annotation: Any):
    model_type = create_test_model(annotation)
    with TestDAOFactory() as daos:
        dao = daos[model_type]
        dao.create_with(id=1, value='TeStVaLuE')

        assert dao.find(value='testvalue').only().id == 1
        assert dao.find(value='TESTVALUE').only().id == 1
        assert dao.find(value='testValue').only().id == 1

        assert dao.find(id=1).only().value == 'TeStVaLuE'
