import inspect
from dataclasses import dataclass
from typing import Any, Callable, TypeVar, Generic

import pytest
from _pytest.outcomes import fail
from sqlalchemy.orm import sessionmaker

from daomodel import DAOModel
from daomodel.dao import NotFound, DAO
from daomodel.db import DAOFactory, create_engine, init_db


T = TypeVar('T')

@dataclass
class Expected(Generic[T]):
    """Wrapper for expected test results to be shared across multiple test cases"""
    value: T

TestCase = tuple
TestGroup = list[Expected | TestCase]
TestCases = TestGroup | TestCase


def _validate_parameters(param_count: int, test_case: TestCase) -> None:
    if param_count > 1:
        if not isinstance(test_case, tuple):
            raise ValueError(f'Expected tuple of {param_count} parameters but got {test_case}')
        elif len(test_case) != param_count:
            raise ValueError(f'Expected {param_count} parameters but got {len(test_case)}: ({test_case})')


def labeled_tests(tests: dict[str, TestCases]):
    def decorator(test_func: Callable):
        parameter_names = inspect.signature(test_func).parameters.keys()
        param_count = len(parameter_names)
        labels = []
        test_data = []

        for group_label, test_cases in tests.items():
            if not isinstance(test_cases, list):
                test_cases = [test_cases]

            expected = None
            try:
                expected_case = next(case for case in test_cases if isinstance(case, Expected))
                expected = expected_case.value
                test_cases.remove(expected_case)
                found_expected = True
            except StopIteration:
                found_expected = False

            for test_case in test_cases if isinstance(test_cases, list) else [test_cases]:
                if found_expected:
                    if isinstance(test_case, tuple):
                        test_case = (*test_case, expected)
                    else:
                        test_case = (test_case, expected)
                _validate_parameters(param_count, test_case)
                labels.append(group_label)
                test_data.append(test_case)
        return pytest.mark.parametrize(', '.join(parameter_names), test_data, ids=labels)(test_func)

    return decorator


class TestDAOFactory(DAOFactory):
    """
    A DAOFactory specifically designed for pytest.
    Includes functionality that can assert what is committed within the DB (through a secondary Session).

    :param debug: If True, uses a test.db file instead of an in-memory SQLite DB. (DB file must be deleted to rerun.
    """
    def __init__(self, debug: bool = False):
        engine = create_engine() if not debug else create_engine('test.db')
        init_db(engine)
        super().__init__(sessionmaker(bind=engine))

    def __enter__(self) -> 'TestDAOFactory':
        super().__enter__()
        return self

    def assert_in_db(self, model: type[DAOModel], *pk, **expected_values: Any) -> None:
        """
        Assert that an object with specific attribute values is present in the DB.
        This checks the committed state of the database, not the session state.

        :param model: The DB table to check
        :param pk: The primary key values of the row
        :param expected_values: The column values to assert
        """
        with self.session_factory() as fresh_session:
            try:
                persisted_copy = DAO(model, fresh_session).get(*pk)
                for key, expected in expected_values.items():
                    actual = getattr(persisted_copy, key)
                    assert actual == expected, f'expected {key} of {persisted_copy} to be {expected} but was {actual}'
            except NotFound as e:
                fail(e.detail)

    def assert_not_in_db(self, model: type[DAOModel], *pk: Any) -> None:
        """
        Assert that the specified object is not present in the DB.
        This checks the committed state of the database, not the session state.

        :param model: The DB table to check
        :param pk: The primary key values of the row
        """
        with self.session_factory() as fresh_session:
            with pytest.raises(NotFound):
                DAO(model, fresh_session).get(*pk)

    def __exit__(self, exc_type, exc_value, traceback):
        super().__exit__(exc_type, exc_value, traceback)
