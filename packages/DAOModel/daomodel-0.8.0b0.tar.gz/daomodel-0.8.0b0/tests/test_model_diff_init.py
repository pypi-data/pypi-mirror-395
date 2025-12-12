from typing import Any

from daomodel import DAOModel
from daomodel.model_diff import ModelDiff
from daomodel.testing import labeled_tests
from tests.test_daomodel import SimpleModel, ComplicatedModel, simple_instance, complicated_instance


@labeled_tests({
    'no diff': [
        (simple_instance, simple_instance, {}),
        (complicated_instance, complicated_instance, {}),
        (complicated_instance, ComplicatedModel(pkC=17, pkD=76, prop1='prop', prop2='erty', fkA=23, fkB=32), {})
    ],
    'single column': [
        (
                simple_instance,
                SimpleModel(pkA=24),
                {'pkA': (23, 24)}
        ), (
                complicated_instance,
                ComplicatedModel(pkC=18, pkD=76, prop1='prop', prop2='erty', fkA=23, fkB=32),
                {'pkC': (17, 18)}
        ), (
                complicated_instance,
                ComplicatedModel(pkC=17, pkD=77, prop1='prop', prop2='erty', fkA=23, fkB=32),
                {'pkD': (76, 77)}
        )
    ],
    'multiple columns': [
        (
                complicated_instance,
                ComplicatedModel(pkC=18, pkD=86, prop1='prop', prop2='erty', fkA=23, fkB=32),
                {'pkC': (17, 18), 'pkD': (76, 86)}
        )
    ]
})
def test_model_diff__init(model: DAOModel, other: DAOModel, expected: dict[str, tuple[Any, Any]]):
    assert ModelDiff(model, other, include_pk=True) == expected


@labeled_tests({
    'no diff': [
        (complicated_instance, complicated_instance, {}),
        (complicated_instance, ComplicatedModel(pkC=17, pkD=76, prop1='prop', prop2='erty', fkA=23, fkB=32), {}),
        (complicated_instance, ComplicatedModel(pkC=18, pkD=77, prop1='prop', prop2='erty', fkA=23, fkB=32), {})
    ],
    'single column': [
        (
                complicated_instance,
                ComplicatedModel(pkC=17, pkD=76, prop1='new', prop2='erty', fkA=23, fkB=32),
                {'prop1': ('prop', 'new')}
        ), (
                complicated_instance,
                ComplicatedModel(pkC=17, pkD=76, prop1='prop', prop2='new', fkA=23, fkB=32),
                {'prop2': ('erty', 'new')}
        ), (
                complicated_instance,
                ComplicatedModel(pkC=17, pkD=76, prop1='prop', prop2='erty', fkA=24, fkB=32),
                {'fkA': (23, 24)}
        ), (
                complicated_instance,
                ComplicatedModel(pkC=17, pkD=76, prop1='prop', prop2='erty', fkA=23, fkB=33),
                {'fkB': (32, 33)}
        )
    ],
    'multiple columns': [
        (
                complicated_instance,
                ComplicatedModel(pkC=17, pkD=76, prop1='new', prop2='prop', fkA=23, fkB=32),
                {'prop1': ('prop', 'new'), 'prop2': ('erty', 'prop')}
        ), (
                complicated_instance,
                ComplicatedModel(pkC=17, pkD=76, prop1='prop', prop2='erty', fkA=0, fkB=0),
                {'fkA': (23, 0), 'fkB': (32, 0)}
        )
    ],
    'none values': [
        (
                complicated_instance,
                ComplicatedModel(pkC=17, pkD=76, prop1='new', prop2=None, fkA=23, fkB=32),
                {'prop1': ('prop', 'new'), 'prop2': ('erty', None)}
        ), (
                ComplicatedModel(pkC=17, pkD=76, prop1='new', prop2=None, fkA=23, fkB=32),
                complicated_instance,
                {'prop1': ('new', 'prop'), 'prop2': (None, 'erty')}
        )
    ],
    'unset values': [
        (
                complicated_instance,
                ComplicatedModel(pkC=17, pkD=76, prop1='new', fkA=23, fkB=32),
                {'prop1': ('prop', 'new'), 'prop2': ('erty', None)}
        ), (
                ComplicatedModel(pkC=17, pkD=76, prop1='new', fkA=23, fkB=32),
                complicated_instance,
                {'prop1': ('new', 'prop'), 'prop2': (None, 'erty')}
        )
    ]
})
def test_model_diff__init__exclude_pk(model: DAOModel, other: DAOModel, expected: dict[str, tuple[Any, Any]]):
    assert ModelDiff(model, other, include_pk=False) == expected
