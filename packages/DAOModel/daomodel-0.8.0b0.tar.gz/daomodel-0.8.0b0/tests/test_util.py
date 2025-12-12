import pytest
from sqlalchemy.testing.schema import Column

from daomodel import reference_of
from daomodel.util import names_of, values_from_dict, retain_in_dict, remove_from_dict, MissingInput
from tests.school_models import Person, Book


@pytest.mark.parametrize('column, expected', [
    (Person.name, 'person.name'),
    (Person.ssn, 'person.ssn'),
    (Book.owner, 'book.owner')
])
def test_reference_of(column: Column, expected: str):
    assert reference_of(column) == expected


@pytest.mark.parametrize('columns, expected', [
    ([], []),
    ([Column('one')], ['one']),
    ([Column('one'), Column('two'), Column('three')], ['one', 'two', 'three'])
])
def test_names_of(columns: list[Column], expected:  list[str]):
    assert names_of(columns) == expected


@pytest.mark.parametrize('keys, expected', [
    ((), ()),
    (('b',), (2,)),
    (('a', 'c'), (1, 3)),
    (('b', 'c', 'a'), (2, 3, 1))
])
def test_values_from_dict(keys: tuple[str, ...], expected: tuple):
    assert values_from_dict(*keys, a=1, b=2, c=3) == expected


def test_values_from_dict__missing():
    with pytest.raises(MissingInput):
        values_from_dict('a', 'b', 'd', a=1, b=2, c=3)


@pytest.mark.parametrize('keys, expected', [
    ((), {}),
    (('b',), {'b': 2}),
    (('a', 'c'), {'a':1, 'c':3}),
    (('b', 'c', 'a'), {'a':1, 'b':2, 'c':3})
])
def test_retain_in_dict(keys: tuple[str, ...], expected: tuple):
    assert retain_in_dict({'a': 1, 'b': 2, 'c': 3}, *keys) == expected


@pytest.mark.parametrize('keys, expected', [
    ((), {'a':1, 'b':2, 'c':3}),
    (('b',), {'a':1, 'c':3}),
    (('a', 'c'), {'b': 2}),
    (('b', 'c', 'a'), {})
])
def test_remove_from_dict(keys: tuple[str, ...], expected: tuple):
    assert remove_from_dict({'a': 1, 'b': 2, 'c': 3}, *keys) == expected
