from decimal import Decimal
from enum import Enum, auto
from typing import Optional, Any

import pytest

from daomodel import DAOModel
from daomodel.fields import Identifier
from daomodel.model_diff import ModelDiff, Preference, PreferenceRule
from daomodel.testing import labeled_tests, Expected


class LaundryStatus(Enum):
    Public = auto()
    Shared = auto()
    Private = auto()


class Rental(DAOModel, table=True):
    address: Identifier[str]
    apt: Identifier[Optional[str]]
    dwelling_type: str
    sqft: int
    bedrooms: int
    bathrooms: Decimal
    garage_parking: int = 0
    laundry: Optional[LaundryStatus]
    cost: int


one_full = Decimal('1')
one_full_one_half = Decimal('1.1')
two_full = Decimal('2')
two_full_two_half = Decimal('2.2')


dorm = Rental(
    address='123 College Ave',
    apt='12',
    dwelling_type='Dormitory',
    sqft=200,
    bedrooms=1,
    bathrooms=one_full,
    laundry=LaundryStatus.Public,
    cost=0
)
apartment = Rental(
    address='456 City Plaza',
    apt='101',
    dwelling_type='Apartment',
    sqft=850,
    bedrooms=2,
    bathrooms=one_full,
    garage_parking=1,
    laundry=LaundryStatus.Shared,
    cost=1200
)
apartment_two = Rental(
    address='456 City Plaza',
    apt='102',
    dwelling_type='Apartment',
    sqft=850,
    bedrooms=2,
    bathrooms=one_full,
    garage_parking=1,
    laundry=LaundryStatus.Shared,
    cost=1200
)
multi_family = Rental(
    address='789 Suburb St',
    apt='B',
    dwelling_type='Multi-family House',
    sqft=950,
    bedrooms=1,
    bathrooms=one_full_one_half,
    cost=1800
)
town_home = Rental(
    address='321 Maple Dr',
    dwelling_type='Town home',
    sqft=1400,
    bedrooms=3,
    bathrooms=two_full,
    garage_parking=1,
    laundry=LaundryStatus.Private,
    cost=2200
)
single_family = Rental(
    address='987 Country Rd',
    dwelling_type='House',
    sqft=1800,
    bedrooms=4,
    bathrooms=two_full_two_half,
    garage_parking=2,
    laundry=LaundryStatus.Private,
    cost=3000
)


def prefer_better_dwelling_type(values: list[str]) -> Preference:
    """Prefer better dwelling types based on predefined categories."""
    left, right = values
    bad = ['Apartment', 'Multi-family House']
    good = ['Town home', 'House']

    def get_value(dwelling_type: str):
        if dwelling_type in bad:
            return -1
        elif dwelling_type in good:
            return 1
        else:
            return 0

    left_value = get_value(left)
    right_value = get_value(right)

    return (
        Preference.LEFT if left_value > right_value else
        Preference.RIGHT if right_value > left_value else
        Preference.BOTH if left_value > 0 else
        Preference.NEITHER
    )

def prefer_more_private(values: list[LaundryStatus]) -> Preference:
    left, right = values
    left_value = 0 if left is None else left.value
    right_value = 0 if right is None else right.value
    return Preference.LEFT if left_value > right_value else Preference.RIGHT

RENTAL_PREFERENCE_RULES = {
    'address': Preference.NOT_APPLICABLE,
    'apt': Preference.NOT_APPLICABLE,
    'default': max,
    'cost': min,
    'dwelling_type': prefer_better_dwelling_type,
    'laundry': prefer_more_private
}


@labeled_tests({
    'dorm vs apartment':
        (dorm, apartment, {
            'dwelling_type': ('Dormitory', 'Apartment'),
            'sqft': (200, 850),
            'bedrooms': (1, 2),
            'garage_parking': (0, 1),
            'laundry': (LaundryStatus.Public, LaundryStatus.Shared),
            'cost': (0, 1200)
        }),
    'dorm vs multi family':
        (dorm, multi_family, {
            'dwelling_type': ('Dormitory', 'Multi-family House'),
            'sqft': (200, 950),
            'bathrooms': (Decimal('1'), Decimal('1.1')),
            'laundry': (LaundryStatus.Public, None),
            'cost': (0, 1800)
        }),
    'dorm vs town home':
        (dorm, town_home, {
            'dwelling_type': ('Dormitory', 'Town home'),
            'sqft': (200, 1400),
            'bedrooms': (1, 3),
            'bathrooms': (Decimal('1'), Decimal('2')),
            'garage_parking': (0, 1),
            'laundry': (LaundryStatus.Public, LaundryStatus.Private),
            'cost': (0, 2200)
        }),
    'dorm vs single family':
        (dorm, single_family, {
            'dwelling_type': ('Dormitory', 'House'),
            'sqft': (200, 1800),
            'bedrooms': (1, 4),
            'bathrooms': (Decimal('1'), Decimal('2.2')),
            'garage_parking': (0, 2),
            'laundry': (LaundryStatus.Public, LaundryStatus.Private),
            'cost': (0, 3000)
        }),
    'apartment vs multi family':
        (apartment, multi_family, {
            'dwelling_type': ('Apartment', 'Multi-family House'),
            'sqft': (850, 950),
            'bedrooms': (2, 1),
            'bathrooms': (Decimal('1'), Decimal('1.1')),
            'garage_parking': (1, 0),
            'laundry': (LaundryStatus.Shared, None),
            'cost': (1200, 1800)
        }),
    'apartment vs town home':
        (apartment, town_home, {
            'dwelling_type': ('Apartment', 'Town home'),
            'sqft': (850, 1400),
            'bedrooms': (2, 3),
            'bathrooms': (Decimal('1'), Decimal('2')),
            'laundry': (LaundryStatus.Shared, LaundryStatus.Private),
            'cost': (1200, 2200)
        }),
    'apartment vs single family':
        (apartment, single_family, {
            'dwelling_type': ('Apartment', 'House'),
            'sqft': (850, 1800),
            'bedrooms': (2, 4),
            'bathrooms': (Decimal('1'), Decimal('2.2')),
            'garage_parking': (1, 2),
            'laundry': (LaundryStatus.Shared, LaundryStatus.Private),
            'cost': (1200, 3000)
        }),
    'multi family vs town home':
        (multi_family, town_home, {
            'dwelling_type': ('Multi-family House', 'Town home'),
            'sqft': (950, 1400),
            'bedrooms': (1, 3),
            'bathrooms': (Decimal('1.1'), Decimal('2')),
            'garage_parking': (0, 1),
            'laundry': (None, LaundryStatus.Private),
            'cost': (1800, 2200)
        }),
    'multi family vs single family':
        (multi_family, single_family, {
            'dwelling_type': ('Multi-family House', 'House'),
            'sqft': (950, 1800),
            'bedrooms': (1, 4),
            'bathrooms': (Decimal('1.1'), Decimal('2.2')),
            'garage_parking': (0, 2),
            'laundry': (None, LaundryStatus.Private),
            'cost': (1800, 3000)
        }),
    'town home vs single family':
        (town_home, single_family, {
            'dwelling_type': ('Town home', 'House'),
            'sqft': (1400, 1800),
            'bedrooms': (3, 4),
            'bathrooms': (Decimal('2'), Decimal('2.2')),
            'garage_parking': (1, 2),
            'cost': (2200, 3000)
        }),
    'empty diff':
        (apartment, apartment_two, {})
})
def test_model_diff(left: Rental, right: Rental, expected: dict[str, tuple[Any, Any]]):
    assert ModelDiff(left, right) == expected


@labeled_tests({
    'same address':
        (apartment, apartment_two, {
            'apt': ('101', '102')
        }),
    'right None':
        (multi_family, town_home, {
            'address': ('789 Suburb St', '321 Maple Dr'),
            'apt': ('B', None)
        }),
    'left None':
        (single_family, multi_family, {
            'address': ('987 Country Rd', '789 Suburb St'),
            'apt': (None, 'B')
        }),
    'both None':
        (town_home, single_family, {
            'address': ('321 Maple Dr', '987 Country Rd')
        })
})
def test_model_diff__pk(left: Rental, right: Rental, expected: dict[str, tuple[Any, Any]]):
    diff = ModelDiff(left, right, include_pk=True)
    pk_diff = {key: diff[key] for key in ['address', 'apt'] if key in diff}
    assert pk_diff == expected


def test_has_left_value_has_right_value():
    diff = ModelDiff(dorm, apartment)
    assert diff.has_left_value('sqft')
    assert diff.has_right_value('sqft')


def test_get_left_get_right():
    diff = ModelDiff(dorm, apartment)
    assert diff.get_left('sqft') == 200
    assert diff.get_right('sqft') == 850


def test_get_left_get_right__missing():
    diff = ModelDiff(apartment, apartment_two)
    with pytest.raises(KeyError):
        diff.get_left('address')
    with pytest.raises(KeyError):
        diff.get_right('cost')


def test_get_left_get_right__invalid():
    diff = ModelDiff(apartment, apartment_two)
    with pytest.raises(KeyError):
        diff.get_left('APT')
    with pytest.raises(KeyError):
        diff.get_right('invalid')


def test_find_rule():
    assert ModelDiff(apartment, apartment_two, **RENTAL_PREFERENCE_RULES)._find_rule('apt') == Preference.NOT_APPLICABLE


@labeled_tests({
    'Preference': [
        Preference.LEFT,
        Preference.RIGHT,
        Preference.BOTH,
        Preference.NEITHER,
        Preference.NOT_APPLICABLE
    ]
})
def test_execute_rule__preference(rule: PreferenceRule):
    assert ModelDiff.execute_rule(rule, ['left', 'right']) == rule


def named_args_rule(left: str, right: str) -> Preference:
    if left == 'good':
        return Preference.LEFT
    elif right == 'good':
        return Preference.RIGHT
    else:
        return Preference.NEITHER


def var_args_rule(*args: str) -> Preference:
    return named_args_rule(args[0], args[1])


def list_arg_rule(values: list[str]) -> Preference:
    return named_args_rule(values[0], values[1])


@labeled_tests({
    'named args': named_args_rule,
    'var args': var_args_rule,
    'list': list_arg_rule,
    'lambda named args': lambda left, right: (
        Preference.LEFT if left == 'good'
        else Preference.RIGHT if right == 'good'
        else Preference.NEITHER
    ),
    'lambda var args': lambda *args: (
        Preference.LEFT if args[0] == 'good'
        else Preference.RIGHT if args[1] == 'good'
        else Preference.NEITHER
    ),
    'lambda list': lambda values: (
        Preference.LEFT if values[0] == 'good'
        else Preference.RIGHT if values[1] == 'good'
        else Preference.NEITHER
    )
})
def test_execute_rule(rule: PreferenceRule):
    assert ModelDiff.execute_rule(rule, ['bad', 'good']) == Preference.RIGHT


@labeled_tests({
    'number': [-1, 0, 1000, 0.5],
    'str': ['a', 'b', 'c', 'left', 'right'],
    'bool': [True, False],
    'none': [None]
})
def test_execute_rule__return_non_preference(value: Any | None):
    assert ModelDiff.execute_rule(lambda _: value, ['left', 'right']) == value


@labeled_tests({
    'already preference': [
        (Preference.LEFT, 'dwelling_type', Preference.LEFT),
        (Preference.RIGHT, 'dwelling_type', Preference.RIGHT),
        (Preference.NEITHER, 'dwelling_type', Preference.NEITHER),
        (Preference.BOTH, 'dwelling_type', Preference.BOTH),
        (Preference.NOT_APPLICABLE, 'dwelling_type', Preference.NOT_APPLICABLE)
    ],
    'equals left value': [Expected(Preference.LEFT),
        ('Dormitory', 'dwelling_type'),
        (200, 'sqft'),
        (1, 'bedrooms'),
        (0, 'garage_parking'),
        (LaundryStatus.Public, 'laundry')
    ],
    'equals right value': [Expected(Preference.RIGHT),
        ('House', 'dwelling_type'),
        (1800, 'sqft'),
        (4, 'bedrooms'),
        (2, 'garage_parking'),
        (LaundryStatus.Private, 'laundry')
    ],
    'equals neither value': [Expected(Preference.NEITHER),
        ('unknown', 'dwelling_type'),
        (1000, 'sqft'),
        (2, 'bedrooms'),
        (3, 'garage_parking'),
        (LaundryStatus.Shared, 'laundry'),
        (None, 'dwelling_type')
    ]
})
def test_map_resolution_to_preference(resolution: Preference | Any | None, field: str, expected: Preference):
    assert ModelDiff(dorm, single_family).map_resolution_to_preference(resolution, field) == expected


def test_get_preferred__not_applicable():
    diff = ModelDiff(multi_family, single_family, include_pk=True, **RENTAL_PREFERENCE_RULES)
    assert diff.get_preferred('address') == Preference.NOT_APPLICABLE
    assert diff.get_preferred('apt') == Preference.NOT_APPLICABLE


def test_get_preferred__not_implemented():
    with pytest.raises(NotImplementedError):
        ModelDiff(apartment, multi_family).get_preferred('cost')


def test_get_preferred__missing():
    with pytest.raises(KeyError):
        ModelDiff(single_family, town_home).get_preferred('laundry')


class RentalDiff(ModelDiff[Rental]):
    def __init__(self, left: Rental, right: Rental):
        super().__init__(left, right, **RENTAL_PREFERENCE_RULES)

@labeled_tests({
    'dorm vs apartment': [
        (dorm, apartment, 'dwelling_type', Preference.LEFT),
        (dorm, apartment, 'sqft', Preference.RIGHT),
        (dorm, apartment, 'bedrooms', Preference.RIGHT),
        (dorm, apartment, 'garage_parking', Preference.RIGHT),
        (dorm, apartment, 'laundry', Preference.RIGHT),
        (dorm, apartment, 'cost', Preference.LEFT)
    ],
    'dorm vs multi family': [
        (dorm, multi_family, 'dwelling_type', Preference.LEFT),
        (dorm, multi_family, 'sqft', Preference.RIGHT),
        (dorm, multi_family, 'bathrooms', Preference.RIGHT),
        (dorm, multi_family, 'laundry', Preference.LEFT),
        (dorm, multi_family, 'cost', Preference.LEFT)
    ],
    'dorm vs town home': [
        (dorm, town_home, 'dwelling_type', Preference.RIGHT),
        (dorm, town_home, 'sqft', Preference.RIGHT),
        (dorm, town_home, 'bedrooms', Preference.RIGHT),
        (dorm, town_home, 'bathrooms', Preference.RIGHT),
        (dorm, town_home, 'garage_parking', Preference.RIGHT),
        (dorm, town_home, 'laundry', Preference.RIGHT),
        (dorm, town_home, 'cost', Preference.LEFT)
    ],
    'dorm vs single family': [
        (dorm, single_family, 'dwelling_type', Preference.RIGHT),
        (dorm, single_family, 'sqft', Preference.RIGHT),
        (dorm, single_family, 'bedrooms', Preference.RIGHT),
        (dorm, single_family, 'bathrooms', Preference.RIGHT),
        (dorm, single_family, 'garage_parking', Preference.RIGHT),
        (dorm, single_family, 'laundry', Preference.RIGHT),
        (dorm, single_family, 'cost', Preference.LEFT)
    ],
    'apartment vs multi family': [
        (apartment, multi_family, 'dwelling_type', Preference.NEITHER),
        (apartment, multi_family, 'sqft', Preference.RIGHT),
        (apartment, multi_family, 'bedrooms', Preference.LEFT),
        (apartment, multi_family, 'bathrooms', Preference.RIGHT),
        (apartment, multi_family, 'garage_parking', Preference.LEFT),
        (apartment, multi_family, 'laundry', Preference.LEFT),
        (apartment, multi_family, 'cost', Preference.LEFT)
    ],
    'apartment vs town home': [
        (apartment, town_home, 'dwelling_type', Preference.RIGHT),
        (apartment, town_home, 'sqft', Preference.RIGHT),
        (apartment, town_home, 'bedrooms', Preference.RIGHT),
        (apartment, town_home, 'bathrooms', Preference.RIGHT),
        (apartment, town_home, 'laundry', Preference.RIGHT),
        (apartment, town_home, 'cost', Preference.LEFT)
    ],
    'apartment vs single family': [
        (apartment, single_family, 'dwelling_type', Preference.RIGHT),
        (apartment, single_family, 'sqft', Preference.RIGHT),
        (apartment, single_family, 'bedrooms', Preference.RIGHT),
        (apartment, single_family, 'bathrooms', Preference.RIGHT),
        (apartment, single_family, 'garage_parking', Preference.RIGHT),
        (apartment, single_family, 'laundry', Preference.RIGHT),
        (apartment, single_family, 'cost', Preference.LEFT)
    ],
    'multi family vs town home': [
        (multi_family, town_home, 'dwelling_type', Preference.RIGHT),
        (multi_family, town_home, 'sqft', Preference.RIGHT),
        (multi_family, town_home, 'bedrooms', Preference.RIGHT),
        (multi_family, town_home, 'bathrooms', Preference.RIGHT),
        (multi_family, town_home, 'garage_parking', Preference.RIGHT),
        (multi_family, town_home, 'laundry', Preference.RIGHT),
        (multi_family, town_home, 'cost', Preference.LEFT)
    ],
    'multi family vs single family': [
        (multi_family, single_family, 'dwelling_type', Preference.RIGHT),
        (multi_family, single_family, 'sqft', Preference.RIGHT),
        (multi_family, single_family, 'bedrooms', Preference.RIGHT),
        (multi_family, single_family, 'bathrooms', Preference.RIGHT),
        (multi_family, single_family, 'garage_parking', Preference.RIGHT),
        (multi_family, single_family, 'laundry', Preference.RIGHT),
        (multi_family, single_family, 'cost', Preference.LEFT)
    ],
    'town home vs single family': [
        (town_home, single_family, 'dwelling_type', Preference.BOTH),
        (town_home, single_family, 'sqft', Preference.RIGHT),
        (town_home, single_family, 'bedrooms', Preference.RIGHT),
        (town_home, single_family, 'bathrooms', Preference.RIGHT),
        (town_home, single_family, 'garage_parking', Preference.RIGHT),
        (town_home, single_family, 'cost', Preference.LEFT)
    ]
})
def test_get_preferred__custom_diff(left: Rental, right: Rental, field: str, expected: Preference):
    assert RentalDiff(left, right).get_preferred(field) == expected
