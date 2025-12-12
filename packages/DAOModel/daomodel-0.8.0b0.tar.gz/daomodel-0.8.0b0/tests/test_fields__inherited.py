from typing import Any, Optional
from uuid import UUID

import pytest
from sqlalchemy.exc import IntegrityError

from daomodel.fields import Protected, Identifier, Unsearchable, no_case_str
from daomodel.list_util import ensure_iter
from daomodel.testing import labeled_tests, TestDAOFactory
from daomodel.util import names_of
from tests.model_factory import create_test_model
from tests.test_fields import BasicModel


all_test_cases = {
    'standard field': str,
    'uuid': UUID,
    'dict': dict,
    'reference': BasicModel,
    'protected reference': Protected[BasicModel],
    'no_case_str': no_case_str,
    'identifier field': Identifier[str],
    'identifier uuid': Identifier[UUID],
    # Note: dict cannot be an Identifier as it is not hashable
    'identifier reference': Identifier[BasicModel],
    'identifier protected reference': Identifier[Protected[BasicModel]],
    'identifier no_case_str': Identifier[no_case_str],
    'optional field': Optional[str],
    'optional uuid': Optional[UUID],
    'optional dict': Optional[dict],
    'optional reference': Optional[BasicModel],
    'optional protected reference': Protected[Optional[BasicModel]],
    'optional no_case_str': Optional[no_case_str],
    'unsearchable field': Unsearchable[str],
    'unsearchable uuid': Unsearchable[UUID],
    'unsearchable dict': Unsearchable[dict],
    'unsearchable reference': Unsearchable[BasicModel],
    'unsearchable protected reference': Unsearchable[Protected[BasicModel]],
    'unsearchable no_case_str': Unsearchable[no_case_str],
    'identifier + optional field': Identifier[Optional[str]],
    'identifier + optional uuid': Identifier[Optional[UUID]],
    # Note: dict cannot be an Identifier as it is not hashable
    'identifier + optional reference': Identifier[Optional[BasicModel]],
    'identifier + optional protected reference': Identifier[Protected[Optional[BasicModel]]],
    'identifier + optional no_case_str': Identifier[Optional[no_case_str]],
    'unsearchable + identifier field': Unsearchable[Identifier[str]],
    'unsearchable + identifier uuid': Unsearchable[Identifier[UUID]],
    # Note: dict cannot be an Identifier as it is not hashable
    'unsearchable + identifier reference': Unsearchable[Identifier[BasicModel]],
    'unsearchable + identifier protected reference': Unsearchable[Identifier[Protected[BasicModel]]],
    'unsearchable + identifier no_case_str': Unsearchable[Identifier[no_case_str]],
    'unsearchable + optional field': Unsearchable[Optional[str]],
    'unsearchable + optional uuid': Unsearchable[Optional[UUID]],
    'unsearchable + optional dict': Unsearchable[Optional[dict]],
    'unsearchable + optional reference': Unsearchable[Optional[BasicModel]],
    'unsearchable + optional protected reference': Unsearchable[Protected[Optional[BasicModel]]],
    'unsearchable + optional no_case_str': Unsearchable[Optional[no_case_str]],
    'unsearchable + identifier + optional field': Unsearchable[Identifier[Optional[str]]],
    'unsearchable + identifier + optional uuid': Unsearchable[Identifier[Optional[UUID]]],
    # Note: dict cannot be an Identifier as it is not hashable
    'unsearchable + identifier + optional reference': Unsearchable[Identifier[Optional[BasicModel]]],
    'unsearchable + identifier + optional protected reference': Unsearchable[Identifier[Protected[Optional[BasicModel]]]],
    'unsearchable + identifier + optional no_case_str': Unsearchable[Identifier[Optional[no_case_str]]]
}


def get_test_cases(*labels: str, exclude: str|tuple[str, ...] = ()) -> dict:
    return {k: v for k, v in all_test_cases.items()
            if all(label in k for label in labels) and not any(ex in k for ex in ensure_iter(exclude))}


@labeled_tests(get_test_cases('field'))
def test_inherited_field(annotation: Any):
    model_type = create_test_model(annotation, inherited=True)
    with TestDAOFactory() as daos:
        dao = daos[model_type]
        dao.create_with(id=1, value='test', child_field='extended')
        entry = dao.find(id=1)
        assert entry.only().value == 'test'
        assert entry.only().child_field == 'extended'


@labeled_tests(get_test_cases('uuid'))
def test_inherited_uuid(annotation: Any):
    model_type = create_test_model(annotation, inherited=True)
    with TestDAOFactory() as daos:
        dao = daos[model_type]
        entry = dao.create_with(id=1, child_field='extended')

        assert getattr(entry, 'value') is not None
        assert isinstance(getattr(entry, 'value'), UUID)

        entry2 = dao.create_with(id=2, child_field='extended')
        assert getattr(entry2, 'value') is not None
        assert isinstance(getattr(entry2, 'value'), UUID)
        assert getattr(entry, 'value') != getattr(entry2, 'value')


@labeled_tests(get_test_cases('dict'))
def test_inherited_dict(annotation: Any):
    model_type = create_test_model(annotation, inherited=True)
    sample_dict = {'Hello': 'World!', 'Lorem': ['Ipsum', 'Dolor', 'Sit', 'Amet']}
    with TestDAOFactory() as daos:
        daos[model_type].create_with(id=1, value=sample_dict, child_field='extended')
        daos.assert_in_db(model_type, 1, value=sample_dict, child_field='extended')


@labeled_tests(get_test_cases('reference'))
def test_inherited_reference(annotation: Any):
    model_type = create_test_model(annotation, inherited=True)
    with TestDAOFactory() as daos:
        daos[BasicModel].create(100)
        dao = daos[model_type]
        dao.create_with(id=1, value=100, child_field='extended')
        entry = dao.find(id=1)
        assert entry.only().value == 100
        assert entry.only().child_field == 'extended'


@labeled_tests(get_test_cases('no_case_str'))
def test_inherited_no_case_str(annotation: Any):
    model_type = create_test_model(annotation, inherited=True)
    with TestDAOFactory() as daos:
        dao = daos[model_type]
        dao.create_with(id=1, value='TeStVaLuE', child_field='extended')
        entry = dao.find(id=1)
        assert entry.only().value == 'TeStVaLuE'
        assert entry.only().child_field == 'extended'


@labeled_tests(get_test_cases(exclude=('optional', 'uuid')))
def test_inherited_required(annotation: Any):
    model_type = create_test_model(annotation, inherited=True)
    with TestDAOFactory() as daos:
        dao = daos[model_type]
        entry = dao.create_with(id=1, child_field='extended', insert=False)
        with pytest.raises(IntegrityError):
            dao.insert(entry)


@labeled_tests(get_test_cases('uuid', exclude='optional'))
def test_inherited_required__uuid(annotation: Any):
    model_type = create_test_model(annotation, inherited=True)
    with TestDAOFactory() as daos:
        dao = daos[model_type]
        dao.create_with(id=1, child_field='extended')
        entry = dao.find(id=1).only()
        # Since UUID has a default value, we test that it is Required by attempting to set it to None
        entry.value = None
        with pytest.raises(IntegrityError):
            dao.upsert(entry)


@labeled_tests(get_test_cases('optional', exclude='uuid'))
def test_inherited_optional(annotation: Any):
    model_type = create_test_model(annotation, inherited=True)
    with TestDAOFactory() as daos:
        dao = daos[model_type]
        dao.create_with(id=1, child_field='extended')
        entry = dao.find(id=1).only()
        assert entry.value is None


@labeled_tests(get_test_cases('optional', 'uuid'))
def test_inherited_optional__uuid(annotation: Any):
    model_type = create_test_model(annotation, inherited=True)
    with TestDAOFactory() as daos:
        dao = daos[model_type]
        dao.create_with(id=1, child_field='extended')
        entry = dao.find(id=1).only()
        assert entry.value is not None
        # Since UUID has a default value, we test that it is Optional by setting it to None
        entry.value = None
        dao.upsert(entry)
        entry = dao.find(id=1).only()
        assert entry.value is None


@labeled_tests(get_test_cases('identifier'))
def test_inherited_identifier(annotation: Any):
    assert create_test_model(annotation, field_name='id2', inherited=True).get_pk_names() == ['id', 'id2']


@labeled_tests(get_test_cases(exclude='unsearchable'))
def test_inherited_searchable(annotation: Any):
    assert names_of(create_test_model(annotation, inherited=True).get_searchable_properties()) == ['id', 'value', 'child_field']


@labeled_tests(get_test_cases('unsearchable'))
def test_inherited_unsearchable(annotation: Any):
    assert names_of(create_test_model(annotation, inherited=True).get_searchable_properties()) == ['id', 'child_field']
