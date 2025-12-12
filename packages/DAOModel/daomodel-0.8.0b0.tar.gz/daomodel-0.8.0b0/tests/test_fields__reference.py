from typing import Optional

import pytest
from sqlalchemy.exc import IntegrityError
from sqlmodel import Field

from daomodel import DAOModel
from daomodel.fields import Identifier, Protected, ReferenceTo
from daomodel.testing import labeled_tests, TestDAOFactory
from tests.test_fields__types import OtherModel


class StandardReferenceModel(DAOModel, table=True):
    id: Identifier[int]
    other_id: OtherModel


class StandardReferenceToModel(DAOModel, table=True):
    id: Identifier[int]
    other_id: int = ReferenceTo('other_model.id')


class OptionalReferenceModel(DAOModel, table=True):
    id: Identifier[int]
    other_id: Optional[OtherModel]


class OptionalReferenceToModel(DAOModel, table=True):
    id: Identifier[int]
    other_id: Optional[int] = ReferenceTo('other_model.id')


class ProtectedReferenceModel(DAOModel, table=True):
    id: Identifier[int]
    other_id: Protected[OtherModel]


class ProtectedReferenceToModel(DAOModel, table=True):
    id: Identifier[int]
    other_id: Protected[int] = ReferenceTo('other_model.id')


class CustomReferenceModel(DAOModel, table=True):
    id: Identifier[int]
    other_id: Optional[OtherModel] = Field(foreign_key='auto', ondelete='CASCADE')


class CustomReferenceToModel(DAOModel, table=True):
    id: Identifier[int]
    other_id: Optional[int] = ReferenceTo('other_model.id', ondelete='CASCADE')


class ReferenceToColumnModel(DAOModel, table=True):
    id: Identifier[int]
    other_id: int = ReferenceTo(OtherModel.id)


class CircularReferenceModel(DAOModel, table=True):
    id: Identifier[int]
    circular: Optional[int] = ReferenceTo('circular_reference_model.id')


class NoTargetReferenceToModel(DAOModel, table=True):
    id: Identifier[int]
    other_id: Optional[OtherModel] = ReferenceTo(ondelete='CASCADE')


class ModelWithUniqueField(DAOModel, table=True):
    id: Identifier[int]
    unique: str = Field(unique=True)


class ReferenceToFieldModel(DAOModel, table=True):
    id: Identifier[int]
    ref: str = ReferenceTo(ModelWithUniqueField.unique)


def test_reference_to(daos: TestDAOFactory):
    daos[OtherModel].create('A')
    daos[StandardReferenceToModel].create_with(id=2, other_id='A')
    daos.assert_in_db(StandardReferenceToModel, 2, other_id='A')


@labeled_tests({
    'reference': StandardReferenceModel,
    'optional reference': OptionalReferenceModel,
    'reference to': StandardReferenceToModel,
    'optional reference to': OptionalReferenceToModel
})
def test_reference__cascade_on_update(model: type[DAOModel]):
    with TestDAOFactory() as daos:
        test_dao = daos[OtherModel]
        fk_dao = daos[model]

        other_entry = test_dao.create('A')
        fk_entry = fk_dao.create_with(id=1, other_id='A')

        test_dao.rename(other_entry, 'B')
        assert fk_entry.other_id == 'B'


@labeled_tests({
    'reference': StandardReferenceModel,
    'optional reference': OptionalReferenceModel,
    'reference to': StandardReferenceToModel,
    'optional reference to': OptionalReferenceToModel
})
def test_reference__cascade_on_delete(model: type[DAOModel]):
    with TestDAOFactory() as daos:
        test_dao = daos[OtherModel]
        fk_dao = daos[model]

        other_entry = test_dao.create('A')
        fk_dao.create_with(id=1, other_id='A')
        daos.assert_in_db(model, 1, other_id='A')

        test_dao.remove(other_entry)
        if model.doc_name().startswith('Optional'):
            daos.assert_in_db(model, 1, other_id=None)
        else:
            daos.assert_not_in_db(model, 1)


@labeled_tests({
    'reference': ProtectedReferenceModel,
    'reference to': ProtectedReferenceToModel
})
def test_reference__protected(model: type[DAOModel]):
    with TestDAOFactory() as daos:
        test_dao = daos[OtherModel]
        fk_dao = daos[model]

        other_entry = test_dao.create('A')
        fk_dao.create_with(id=1, other_id='A')

        with pytest.raises(IntegrityError):
            test_dao.remove(other_entry)


@labeled_tests({
    'reference': CustomReferenceModel,
    'reference to': CustomReferenceToModel
})
def test_reference__override_on_delete(model: type[DAOModel]):
    with TestDAOFactory() as daos:
        test_dao = daos[OtherModel]
        fk_dao = daos[model]

        fk_entry = fk_dao.create(1)
        daos.assert_in_db(model, 1, other_id=None)

        other_entry = test_dao.create('A')
        fk_entry.other_id = other_entry.id
        fk_dao.upsert(fk_entry)
        daos.assert_in_db(model, 1, other_id='A')

        test_dao.remove(other_entry)
        daos.assert_not_in_db(model, 1)


def test_reference_to__column(daos: TestDAOFactory):
    daos[OtherModel].create('A')
    daos[ReferenceToColumnModel].create_with(id=2, other_id='A')
    daos.assert_in_db(ReferenceToColumnModel, 2, other_id='A')


def test_reference_to__self(daos: TestDAOFactory):
    daos[CircularReferenceModel].create(1)
    daos[CircularReferenceModel].create_with(id=2, circular=1)
    daos.assert_in_db(CircularReferenceModel, 2, circular=1)


def test_reference_to__no_target(daos: TestDAOFactory):
    other = daos[OtherModel].create('A')
    daos[NoTargetReferenceToModel].create_with(id=1, other_id='A')
    daos.assert_in_db(NoTargetReferenceToModel, 1, other_id='A')

    daos[OtherModel].remove(other)
    daos.assert_not_in_db(NoTargetReferenceToModel, 1)


def test_reference_to__unique_field(daos: TestDAOFactory):
    daos[ModelWithUniqueField].create_with(id=0, unique='value')
    daos[ReferenceToFieldModel].create_with(id=1, ref='value')
    daos.assert_in_db(ReferenceToFieldModel, 1, ref='value')
