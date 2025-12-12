from typing import Optional, Any

import pytest

from daomodel import DAOModel
from daomodel.fields import Identifier
from daomodel.property_filter import PropertyFilter, BasicPropertyFilter, AndFilter, ALL, PK, FK, DEFAULT, NONE
from daomodel.testing import labeled_tests


class ForeignModel(DAOModel, table=True):
    pk: Identifier[int]


class PropertyModel(DAOModel, table=True):
    pk_value: Identifier[int]
    pk_default_none: Identifier[Optional[int]]
    pk_default: Identifier[int] = 0
    pk_override: Identifier[int] = 0
    pk_default_optional: Identifier[Optional[int]] = 0
    pk_override_optional: Identifier[Optional[int]] = 0
    pk_override_none: Identifier[Optional[int]] = 0

    pk_fk_value: Identifier[ForeignModel]
    pk_fk_default_none: Identifier[Optional[ForeignModel]]
    pk_fk_default: Identifier[ForeignModel] = 0
    pk_fk_override: Identifier[ForeignModel] = 0
    pk_fk_default_optional: Identifier[Optional[ForeignModel]] = 0
    pk_fk_override_optional: Identifier[Optional[ForeignModel]] = 0
    pk_fk_override_none: Identifier[Optional[ForeignModel]] = 0

    fk_value: ForeignModel
    fk_default_none: Optional[ForeignModel]
    fk_default: ForeignModel = 0
    fk_override: ForeignModel = 0
    fk_default_optional: Optional[ForeignModel] = 0
    fk_override_optional: Optional[ForeignModel] = 0
    fk_override_none: Optional[ForeignModel] = 0

    field_value: int
    field_default_none: Optional[int]
    field_default: int = 0
    field_override: int = 0
    field_default_optional: Optional[int] = 0
    field_override_optional: Optional[int] = 0
    field_override_none: Optional[int] = 0


property_model = PropertyModel(
    pk_value=1,
    pk_override=1,
    pk_override_optional=1,
    pk_override_none=None,

    pk_fk_value=1,
    pk_fk_override=1,
    pk_fk_override_optional=1,
    pk_fk_override_none=None,

    fk_value=1,
    fk_override=1,
    fk_override_optional=1,
    fk_override_none=None,

    field_value=1,
    field_override=1,
    field_override_optional=1,
    field_override_none=None,
)

all_properties = [
    'pk_value',
    'pk_default_none',
    'pk_default',
    'pk_override',
    'pk_default_optional',
    'pk_override_optional',
    'pk_override_none',

    'pk_fk_value',
    'pk_fk_default_none',
    'pk_fk_default',
    'pk_fk_override',
    'pk_fk_default_optional',
    'pk_fk_override_optional',
    'pk_fk_override_none',

    'fk_value',
    'fk_default_none',
    'fk_default',
    'fk_override',
    'fk_default_optional',
    'fk_override_optional',
    'fk_override_none',

    'field_value',
    'field_default_none',
    'field_default',
    'field_override',
    'field_default_optional',
    'field_override_optional',
    'field_override_none'
]

@pytest.mark.parametrize('property_filter, expected', [
    (ALL, all_properties),
    (PK, {name for name in all_properties if 'pk_' in name}),
    (FK, {name for name in all_properties if 'fk_' in name}),
    (DEFAULT, {name for name in all_properties if 'default' in name}),
    (NONE, {name for name in all_properties if 'none' in name})
])
def test_basic_filter(property_filter: BasicPropertyFilter, expected: list[str]):
    assert property_filter.evaluate(property_model) == set(expected)

@pytest.mark.parametrize('property_filter', [ALL, PK, FK, DEFAULT, NONE])
def test_not_filter(property_filter: BasicPropertyFilter):
    normal_filter = property_filter.evaluate(property_model)
    not_filter = (~property_filter).evaluate(property_model)
    assert normal_filter.isdisjoint(not_filter)
    assert normal_filter | not_filter == set(all_properties)

@pytest.mark.parametrize('property_filter', [ALL, PK, FK, DEFAULT, NONE])
def test_or_filter(property_filter: BasicPropertyFilter):
    assert (property_filter | ~property_filter).evaluate(property_model) == set(all_properties)

@pytest.mark.parametrize('property_filter, expected', [
    (PK & FK, {name for name in all_properties if 'pk_fk_' in name}),
    (DEFAULT & NONE, {'pk_default_none', 'pk_fk_default_none', 'fk_default_none', 'field_default_none'}),
    (PK & DEFAULT, {'pk_default_none', 'pk_default', 'pk_default_optional', 'pk_fk_default_none', 'pk_fk_default', 'pk_fk_default_optional'}),
    (FK & NONE, {'pk_fk_default_none', 'pk_fk_override_none', 'fk_default_none', 'fk_override_none'}),
])
def test_and_filter(property_filter: AndFilter, expected: list[str]):
    assert property_filter.evaluate(property_model) == set(expected)

def test_evaluate_to_no_results():
    assert (~ALL).evaluate(property_model) == set()

@labeled_tests({
    'modified to None':
        (~DEFAULT & NONE, {'pk_override_none', 'pk_fk_override_none', 'fk_override_none', 'field_override_none'}),
    'existing relationships':
        (FK & ~NONE, {
            'pk_fk_value',
            'pk_fk_default',
            'pk_fk_override',
            'pk_fk_default_optional',
            'pk_fk_override_optional',

            'fk_value',
            'fk_default',
            'fk_override',
            'fk_default_optional',
            'fk_override_optional'
        }),
    'standard fields':
        (~PK & ~FK, {name for name in all_properties if 'field_' in name}),
    'keys':
        (PK | FK, {
            'pk_value',
            'pk_default_none',
            'pk_default',
            'pk_override',
            'pk_default_optional',
            'pk_override_optional',
            'pk_override_none',

            'pk_fk_value',
            'pk_fk_default_none',
            'pk_fk_default',
            'pk_fk_override',
            'pk_fk_default_optional',
            'pk_fk_override_optional',
            'pk_fk_override_none',

            'fk_value',
            'fk_default_none',
            'fk_default',
            'fk_override',
            'fk_default_optional',
            'fk_override_optional',
            'fk_override_none'
        }),
    'fields that are primary and non-null or foreign and default':
        (PK & ~NONE | FK & DEFAULT, {
            'pk_value',
            'pk_default',
            'pk_override',
            'pk_default_optional',
            'pk_override_optional',

            'pk_fk_value',
            'pk_fk_default_none',
            'pk_fk_default',
            'pk_fk_override',
            'pk_fk_default_optional',
            'pk_fk_override_optional',

            'fk_default_none',
            'fk_default',
            'fk_default_optional'
        }),
    'non-keys with a modified value that is not None':
        (~FK & ~PK & ~DEFAULT & ~NONE, {'field_value', 'field_override', 'field_override_optional'}),
    'default fields except unset optional unless it is pk fk or not a key at all':
        (DEFAULT & ~(NONE & DEFAULT & ~(PK & FK | ~(PK | FK))), {
            'pk_default',
            'pk_default_optional',

            'pk_fk_default_none',
            'pk_fk_default',
            'pk_fk_default_optional',

            'fk_default',
            'fk_default_optional',

            'field_default_none',
            'field_default',
            'field_default_optional',
        })
})
def test_mixed_filters(property_filter: PropertyFilter, expected: set[str]):
    assert property_filter.evaluate(property_model) == expected

@labeled_tests({
    'primary key properties':
        (PK, [
            'pk_value',
            'pk_default_none',
            'pk_default',
            'pk_override',
            'pk_default_optional',
            'pk_override_optional',
            'pk_override_none',

            'pk_fk_value',
            'pk_fk_default_none',
            'pk_fk_default',
            'pk_fk_override',
            'pk_fk_default_optional',
            'pk_fk_override_optional',
            'pk_fk_override_none'
        ]),
    'foreign but not primary key properties':
        (FK & ~PK, [
            'fk_value',
            'fk_default_none',
            'fk_default',
            'fk_override',
            'fk_default_optional',
            'fk_override_optional',
            'fk_override_none'
        ])
})
def test_get_property_names(property_filter: PropertyFilter, expected: list[str]):
    assert property_model.get_property_names(property_filter) == expected

def test_get_property_names__no_args():
    assert property_model.get_property_names() == all_properties

def test_get_property_names__multiple_args():
    assert property_model.get_property_names(~PK, ~FK, ~NONE | DEFAULT) == [
        'field_value',
        'field_default_none',
        'field_default',
        'field_override',
        'field_default_optional',
        'field_override_optional'
    ]

@labeled_tests({
    'standard properties':
        (~(PK | FK), {
            'field_value': 1,
            'field_default_none': None,
            'field_default': 0,
            'field_override': 1,
            'field_default_optional': 0,
            'field_override_optional': 1,
            'field_override_none': None
        }),
    'no properties':
        (PK & ~PK, dict())
})
def test_get_property_values(property_filter: PropertyFilter, expected: dict[str, Any]):
    assert property_model.get_property_values(property_filter) == expected
