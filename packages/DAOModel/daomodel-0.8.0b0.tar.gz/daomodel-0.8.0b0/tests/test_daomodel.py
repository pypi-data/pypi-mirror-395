from typing import Iterable, Any, Optional

import pytest
from sqlalchemy import Column
from sqlmodel import Field

from daomodel import DAOModel, names_of, UnsearchableError, reference_of, ColumnBreadcrumbs
from daomodel.fields import Identifier, Unsearchable
from daomodel.testing import labeled_tests, Expected


class Model(DAOModel):
    pass


class SimpleModel(DAOModel, table=True):
    pkA: Identifier[int]

simple_instance = SimpleModel(pkA=23)


class ForeignKEYModel(DAOModel, table=True):
    pkB: Identifier[int]
    prop: str
    sensitive_prop: Unsearchable[str]
    fk: SimpleModel


class BaseModel(DAOModel):
    prop1: str


class ComplicatedModel(BaseModel, table=True):
    pkC: Identifier[int]
    pkD: Identifier[int]
    prop2: Unsearchable[Optional[str]]
    fkA: int = Field(foreign_key='simple_model.pkA')
    fkB: int = Field(foreign_key='foreign_key_model.pkB')

    class Meta:
        searchable_relations = {
            ForeignKEYModel.prop,
            ForeignKEYModel.sensitive_prop,
            (ForeignKEYModel, SimpleModel.pkA)
        }

complicated_instance = ComplicatedModel(pkC=17, pkD=76, prop1='prop', prop2='erty', fkA=23, fkB=32)


class MultiForeignKEYModel(DAOModel, table=True):
    fkC: int = Field(primary_key=True, foreign_key='complicated_model.pkC')
    fkD: int = Field(primary_key=True, foreign_key='complicated_model.pkD')
    fk_prop: str = Field(foreign_key='foreign_key_model.prop')


def test_tablename():
    assert SimpleModel.__tablename__ == 'simple_model'
    assert ForeignKEYModel.__tablename__ == 'foreign_key_model'


@labeled_tests({
    'true': [
        (SimpleModel, SimpleModel.pkA, True),
        (ForeignKEYModel, ForeignKEYModel.pkB, True),
        (ForeignKEYModel, ForeignKEYModel.prop, True),
        (ForeignKEYModel, ForeignKEYModel.fk, True),
        (ComplicatedModel, ComplicatedModel.pkC, True),
        (ComplicatedModel, ComplicatedModel.pkD, True),
        (ComplicatedModel, ComplicatedModel.prop1, True),
        (ComplicatedModel, ComplicatedModel.prop2, True),
        (ComplicatedModel, ComplicatedModel.fkA, True),
        (ComplicatedModel, ComplicatedModel.fkB, True),
        (MultiForeignKEYModel, MultiForeignKEYModel.fkC, True),
        (MultiForeignKEYModel, MultiForeignKEYModel.fkD, True),
        (MultiForeignKEYModel, MultiForeignKEYModel.fk_prop, True)
    ],
    'false': [
        (SimpleModel, ForeignKEYModel.pkB, False),
        (SimpleModel, ForeignKEYModel.prop, False),
        (SimpleModel, ComplicatedModel.pkC, False),
        (SimpleModel, ComplicatedModel.pkD, False),
        (SimpleModel, ComplicatedModel.prop1, False),
        (SimpleModel, ComplicatedModel.prop2, False),
        (SimpleModel, ComplicatedModel.fkB, False),
        (SimpleModel, MultiForeignKEYModel.fk_prop, False),
        (ForeignKEYModel, ComplicatedModel.pkC, False),
        (ForeignKEYModel, ComplicatedModel.pkD, False),
        (ForeignKEYModel, ComplicatedModel.prop1, False),
        (ForeignKEYModel, ComplicatedModel.prop2, False),
        (ForeignKEYModel, ComplicatedModel.fkA, False),
        (ForeignKEYModel, MultiForeignKEYModel.fkC, False),
        (ForeignKEYModel, MultiForeignKEYModel.fkD, False),
        (ComplicatedModel, ForeignKEYModel.prop, False),
        (ComplicatedModel, MultiForeignKEYModel.fk_prop, False),
        (MultiForeignKEYModel, SimpleModel.pkA, False),
        (MultiForeignKEYModel, ComplicatedModel.prop1, False),
        (MultiForeignKEYModel, ComplicatedModel.prop2, False),
        (MultiForeignKEYModel, ComplicatedModel.fkA, False),
        (MultiForeignKEYModel, ComplicatedModel.fkB, False)
    ],
    'foreign keys': [
        (ForeignKEYModel, SimpleModel.pkA, False),
        (ComplicatedModel, SimpleModel.pkA, False),
        (ComplicatedModel, ForeignKEYModel.pkB, False),
        (MultiForeignKEYModel, ComplicatedModel.pkC, False),
        (MultiForeignKEYModel, ComplicatedModel.pkD, False),
        (MultiForeignKEYModel, ForeignKEYModel.prop, False)
    ],
    'foreign references': [
        (SimpleModel, ForeignKEYModel.fk, False),
        (ForeignKEYModel, ComplicatedModel.fkB, False),
        (ForeignKEYModel, MultiForeignKEYModel.fk_prop, False),
        (ComplicatedModel, MultiForeignKEYModel.fkC, False),
        (ComplicatedModel, MultiForeignKEYModel.fkD, False)
    ],
    'inherited': [
        (ComplicatedModel, ComplicatedModel.prop1, True),
        (BaseModel, ComplicatedModel.prop1, False),
        (BaseModel, ComplicatedModel.prop2, False)
    ]
})
def test_has_column(model: DAOModel, column: Column, expected: bool):
    assert model.has_column(column) is expected


@labeled_tests({
    'single word':
        (Model, 'model'),
    'multiple words': [
        (SimpleModel, 'simple_model'),
        (ComplicatedModel, 'complicated_model')
    ],
    'acronym': [
        (ForeignKEYModel, 'foreign_key_model'),
        (MultiForeignKEYModel, 'multi_foreign_key_model')
    ]
})
def test_normalized_name(model: type[DAOModel], expected: str):
    assert model.normalized_name() == expected


@labeled_tests({
    'single word':
        (Model, 'Model'),
    'multiple words': [
        (SimpleModel, 'Simple Model'),
        (ComplicatedModel, 'Complicated Model')
    ],
    'acronym': [
        (ForeignKEYModel, 'Foreign Key Model'),
        (MultiForeignKEYModel, 'Multi Foreign Key Model')
    ]
})
def test_doc_name(model: type[DAOModel], expected: str):
    assert model.doc_name() == expected


@labeled_tests({
    'single column':
        (SimpleModel, ['pkA']),
    'multiple columns':
        (ComplicatedModel, ['pkC', 'pkD'])
})
def test_get_pk_names__single_column(model: type[DAOModel], expected: list[str]):
    assert model.get_pk_names() == expected


@labeled_tests({
    'single column':
        (simple_instance, (23,)),
    'multiple columns':
        (complicated_instance, (17, 76))
})
def test_get_pk_values(model: DAOModel, expected: tuple[int, ...]):
    assert model.get_pk_values() == expected


@labeled_tests({
    'single column':
        (simple_instance, {'pkA': 23}),
    'multiple columns':
        (complicated_instance, {'pkC': 17, 'pkD': 76})
})
def test_get_pk_dict(model: DAOModel, expected: dict[str, int]):
    assert model.get_pk_dict() == expected


@labeled_tests({
    'single column':
        (ForeignKEYModel, {'pkA'}),
    'multiple columns':
        (ComplicatedModel, {'pkA', 'pkB'})
})
def test_get_fks(model: type[DAOModel], expected: set[str]):
    assert set(names_of(model.get_fks())) == expected


@labeled_tests({
    'single column':
        (ForeignKEYModel, {'fk'}),
    'multiple columns':
        (ComplicatedModel, {'fkA', 'fkB'})
})
def test_get_fk_properties(model: type[DAOModel], expected: set[str]):
    assert set(names_of(model.get_fk_properties())) == expected


def to_str(columns: Iterable[Column]):
    """Converts columns to strings instead to make assert comparisons simpler"""
    return {reference_of(column) for column in columns}


@labeled_tests({
    'single column':
        (ForeignKEYModel, SimpleModel, {ForeignKEYModel.fk}),
    'some applicable columns': [
        (ComplicatedModel, SimpleModel, {ComplicatedModel.fkA}),
        (ComplicatedModel, ForeignKEYModel, {ComplicatedModel.fkB})
    ],
    'no applicable columns':
        (MultiForeignKEYModel, SimpleModel, {}),
    'non primary key':
        (MultiForeignKEYModel, ForeignKEYModel, {MultiForeignKEYModel.fk_prop}),
    'multiple columns':
        (MultiForeignKEYModel, ComplicatedModel, {MultiForeignKEYModel.fkC, MultiForeignKEYModel.fkD})
})
def test_get_references_of(model: type[DAOModel], reference: type[DAOModel], expected: set[Column]):
    assert to_str([fk.parent for fk in model.get_references_of(reference)]) == to_str(expected)


@labeled_tests({
    'single column':
        (SimpleModel, ['pkA']),
    'multiple columns':
        (ForeignKEYModel, ['pkB', 'prop', 'sensitive_prop', 'fk']),
    'inherited columns':
        (ComplicatedModel, ['prop1', 'pkC', 'pkD', 'prop2', 'fkA', 'fkB'])
})
def test_get_properties(model: type[DAOModel], expected: list[str]):
    assert names_of(model.get_properties()) == expected


class ModelWithDefaults(DAOModel, table=True):
    default_of_abc: Identifier[str] = 'abc'
    default_of_123: int = 123
    default_of_false: bool = False
    default_of_none: str = None


@labeled_tests({
    'by column': [
        (ModelWithDefaults.default_of_abc, 'abc'),
        (ModelWithDefaults.default_of_123, 123),
        (ModelWithDefaults.default_of_false, False)
    ],
    'by column name':[
        ('default_of_abc', 'abc'),
        ('default_of_123', 123),
        ('default_of_false', False)
    ],
    'optional column (default=None)':
        (ModelWithDefaults.default_of_none, None)
})
def test_get_default(column: Column|str, expected: Any):
    assert ModelWithDefaults.get_default(column) == expected


def test_get_default__no_default():
    with pytest.raises(ValueError):
        SimpleModel.get_default(SimpleModel.pkA)


@labeled_tests({
    'primary key': [
        (simple_instance, SimpleModel.pkA, 23),
        (complicated_instance, ComplicatedModel.pkC, 17),
        (complicated_instance, ComplicatedModel.pkD, 76)
    ],
    'foreign key': [
        (complicated_instance, ComplicatedModel.fkA, 23),
        (complicated_instance, ComplicatedModel.fkB, 32)
    ],
    'inherited column':
        (complicated_instance, ComplicatedModel.prop1, 'prop'),
    'standard column':
        (complicated_instance, ComplicatedModel.prop2, 'erty'),
    'by str':
        (complicated_instance, 'prop2', 'erty')
})
def test_get_value_of(model: DAOModel, column: Column|str, expected: Any):
    assert model.get_value_of(column) == expected


@labeled_tests({
    'no columns': [
        (simple_instance, [], {}),
        (complicated_instance, [], {})
    ],
    'single column': [
        (simple_instance, ['pkA'], {'pkA': 23}),
        (complicated_instance, ['pkC'], {'pkC': 17}),
        (complicated_instance, ['pkD'], {'pkD': 76}),
        (complicated_instance, ['prop1'], {'prop1': 'prop'}),
        (complicated_instance, ['prop2'], {'prop2': 'erty'}),
        (complicated_instance, ['fkA'], {'fkA': 23}),
        (complicated_instance, ['fkB'], {'fkB': 32}),
    ],
    'multiple columns':
        (complicated_instance, ['pkC', 'pkD', 'prop1', 'prop2', 'fkA', 'fkB'], {
            'pkC': 17,
            'pkD': 76,
            'prop1': 'prop',
            'prop2': 'erty',
            'fkA': 23,
            'fkB': 32
        })
})
def test_get_values_of(model: DAOModel, columns: list[Column], expected: Any):
    assert model.get_values_of(columns) == expected


@labeled_tests({
    'single column':
        (SimpleModel, ['pkA']),
    'multiple columns':
        (ForeignKEYModel, ['pkB', 'prop', 'fk'])
})
def test_get_searchable_properties(model: type[DAOModel], expected: list[str]):
    assert names_of(model.get_searchable_properties()) == expected


@labeled_tests({
    'mapped relation': ForeignKEYModel.prop,
    'unsearchable mapped relation': ForeignKEYModel.sensitive_prop,
    'breadcrumbs': (ForeignKEYModel, SimpleModel.pkA)
})
def test_get_searchable_properties__meta(expected: Column | ColumnBreadcrumbs):
    assert expected in ComplicatedModel.get_searchable_properties()


@labeled_tests({
    'column': [ Expected([]),
        ComplicatedModel.pkC,
        ComplicatedModel.pkD,
        ComplicatedModel.prop1,
        ComplicatedModel.fkA,
        ComplicatedModel.fkB
    ],
    'column reference': [ Expected([]),
        'complicated_model.pkC',
        'complicated_model.pkD',
        'complicated_model.prop1',
        'complicated_model.fkA',
        'complicated_model.fkB'
    ],
    'column name': [ Expected([]),
        'pkC',
        'pkD',
        'prop1',
        'fkA',
        'fkB'
    ],
    'foreign property': [ Expected([ForeignKEYModel.normalized_name()]),
        ForeignKEYModel.prop,
        'foreign_key_model.prop'
    ],
    'nested foreign property': [ Expected([ForeignKEYModel.normalized_name(), SimpleModel.normalized_name()]),
        SimpleModel.pkA,
        'simple_model.pkA'
    ]
})
def test_find_searchable_column(prop: str|Column, expected: list[str]):
    foreign_tables = []
    assert ComplicatedModel.find_searchable_column(prop, foreign_tables) is not None
    assert [t.name for t in foreign_tables] == expected


def test_find_searchable_column__foreign_without_table():
    with pytest.raises(UnsearchableError):
        ComplicatedModel.find_searchable_column('prop', [])


@labeled_tests({
    'single column':
        (SimpleModel, (23,), {'pkA': 23}),
    'multiple columns':
        (ComplicatedModel, (17, 76), {'pkC': 17, 'pkD': 76})
})
def test_pk_values_to_dict__single_column(model: type[DAOModel], args: tuple[int, ...], expected: dict[str, int]):
    assert model.pk_values_to_dict(args) == expected


def test_copy_model():
    other = ComplicatedModel(pkC=12, pkD=34, prop1='different', prop2='values', fkA=1, fkB=2)
    other.copy_model(complicated_instance)
    assert other.pkC == 12
    assert other.pkD == 34
    assert other.prop1 == 'prop'
    assert other.prop2 == 'erty'
    assert other.fkA == 23
    assert other.fkB == 32
    assert complicated_instance.pkC == 17
    assert complicated_instance.pkD == 76
    assert complicated_instance.prop1 == 'prop'
    assert complicated_instance.prop2 == 'erty'
    assert complicated_instance.fkA == 23
    assert complicated_instance.fkB == 32


def test_copy_model__specific_fields():
    other = ComplicatedModel(pkC=12, pkD=34, prop1='different', prop2='values', fkA=1, fkB=2)
    other.copy_model(complicated_instance, 'prop1', 'fkA')
    assert other.pkC == 12
    assert other.pkD == 34
    assert other.prop1 == 'prop'
    assert other.prop2 == 'values'
    assert other.fkA == 23
    assert other.fkB == 2


def test_copy_model__pk():
    other = ComplicatedModel(pkC=12, pkD=34, prop1='different', prop2='values', fkA=1, fkB=2)
    other.copy_model(complicated_instance, 'pkD')
    assert other.pkC == 12
    assert other.pkD == 76
    assert other.prop1 == 'different'
    assert other.prop2 == 'values'
    assert other.fkA == 1
    assert other.fkB == 2


def test_set_values():
    other = ComplicatedModel(pkC=12, pkD=34, prop1='different', prop2='values', fkA=1, fkB=2)
    other.set_values(prop1='new', fkB=3)
    assert other.model_dump() == {
        'pkC': 12,
        'pkD': 34,
        'prop1': 'new',
        'prop2': 'values',
        'fkA': 1,
        'fkB': 3
    }


def test_set_values__extra_values():
    other = ComplicatedModel(pkC=12, pkD=34, prop1='different', prop2='values', fkA=1, fkB=2)
    other.set_values(prop1='new', other='extra')
    assert other.model_dump() == {
        'pkC': 12,
        'pkD': 34,
        'prop1': 'new',
        'prop2': 'values',
        'fkA': 1,
        'fkB': 2
    }


def test_set_values__ignore_pk():
    other = ComplicatedModel(pkC=12, pkD=34, prop1='different', prop2='values', fkA=1, fkB=2)
    other.set_values(ignore_pk=True, pkC=0, prop1='new')
    assert other.model_dump() == {
        'pkC': 12,
        'pkD': 34,
        'prop1': 'new',
        'prop2': 'values',
        'fkA': 1,
        'fkB': 2
    }


def test_set_values__pk():
    other = ComplicatedModel(pkC=12, pkD=34, prop1='different', prop2='values', fkA=1, fkB=2)
    other.set_values(pkC=0)
    assert other.model_dump() == {
        'pkC': 0,
        'pkD': 34,
        'prop1': 'different',
        'prop2': 'values',
        'fkA': 1,
        'fkB': 2
    }


@labeled_tests({
    'single column': (
            simple_instance,
            SimpleModel(pkA=23),
            (
                    SimpleModel(pkA=32),
                    SimpleModel(pkA=45)
            )
    ),
    'multiple columns': (
            complicated_instance,
            ComplicatedModel(pkC=17, pkD=76, prop1='different', prop2='values', fkA=1, fkB=2),
            (
                    ComplicatedModel(pkC=17, pkD=89, prop1='prop', prop2='erty', fkA=23, fkB=32),
                    ComplicatedModel(pkC=17, pkD=89, prop1='prop', prop2='erty', fkA=23, fkB=32)
            )
    )
})
def test___eq____hash__(model: DAOModel, equivalent: DAOModel, different: tuple[DAOModel, ...]):
    assert model == equivalent
    assert hash(model) == hash(equivalent)
    for instance in different:
        assert model != instance
        assert hash(model) != hash(instance)


@labeled_tests({
    'single column':
        (simple_instance, '23'),
    'multiple columns':
        (complicated_instance, '(17, 76)')
})
def test___str___single_column(model: DAOModel, expected: str):
    assert str(model) == expected
