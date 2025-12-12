from typing import Any, Iterable, Optional

import pytest

from daomodel.list_util import (
    most_frequent, ensure_iter, dedupe, in_order, strip_whitespace, exclude_falsy, first_str_with, first, last, longest
)
from daomodel.testing import labeled_tests


@labeled_tests({
    'already iterable': [
        ([1, 2, 3], [1, 2, 3]),
        ({1, 2, 3}, {1, 2, 3}),
        ((1, 2, 3), (1, 2, 3))
    ],
    'empty': [
        ([], []),
        ({}, {}),
        ((), ()),
    ],
    'single item': [
        (1, [1]),
        (None, [None]),
        ('element', ['element']),
    ]
})
def test_ensure_iter(elements: Any, expected: Iterable[Any]):
    assert ensure_iter(elements) == expected


@labeled_tests({
    'empty': [
        (set(), [], []),
        (set(), [1], []),
        ({1}, [], []),
    ],
    'single item': [
        ({1}, [1], [1]),
        ({'a'}, ['a'], ['a'])
    ],
    'multiple items': [
        ({1, 2, 3}, [1, 2, 3], [1, 2, 3]),
        ({1, 2, 3}, [3, 2, 1], [3, 2, 1]),
        ({'a', 'b', 'c'}, ['a', 'b', 'c'], ['a', 'b', 'c']),
        ({'a', 'b', 'c'}, ['c', 'b', 'a'], ['c', 'b', 'a'])
    ],
    'repeated items': [
        ([1, 1, 2, 2, 3, 3], [1, 2, 3], [1, 2, 3]),
        ([1, 1, 2, 2, 3, 3], [3, 2, 1], [3, 2, 1]),
        (['a', 'b', 'c', 'b', 'a'], ['a', 'b', 'c'], ['a', 'b', 'c']),
        (['a', 'b', 'c', 'b', 'a'], ['c', 'b', 'a'], ['c', 'b', 'a']),
        ([True, True, False, True, False, False], [False, True], [False, True])
    ],
    'items missing from order': [
        ({1, 2, 3, 4}, [1, 2, 3], [1, 2, 3]),
        ({1, 2, 3, 4}, [3, 2, 1], [3, 2, 1])
    ],
    'extraneous items in order': [
        ({1, 3}, [1, 2, 3], [1, 3]),
        ({1, 3}, [3, 2, 1], [3, 1])
    ],
    'mixed scenarios': [
        ({4, 1, 1, 3, 4}, [1, 2, 3], [1, 3]),
        ({1, 3, 1, 4}, [3, 2, 1], [3, 1])
    ]
})
def test_in_order(items: Iterable, order: list, expected: list):
    assert in_order(items, order) == expected


@pytest.mark.parametrize('elements, expected', [
    ([1, 2, 3], [1, 2, 3]),
    ([1, 1, 2, 2, 3, 3, 3], [1, 2, 3]),
    (['one', 'two', 'two', 'three'], ['one', 'two', 'three']),
    (['one', 1, 'one', 'two', 2, 'three', 2, 'three', 2], ['one', 1, 'two', 2, 'three']),
    ([], []),
])
def test_dedupe(elements: list, expected: list):
    assert dedupe(elements) == expected


def test_dedupe__keep_last():
    elements = ['one', 1, 'one', 'two', 2, 'three', 2, 'three', 2]
    expected = [1, 'one', 'two', 'three', 2]
    assert dedupe(elements, keep_last=True) == expected


@pytest.mark.parametrize('elements, expected', [
    (['  test  ', ' example ', 'no trim'], ['test', 'example', 'no trim']),
    (['  leading', 'trailing  ', '  both  '], ['leading', 'trailing', 'both']),
    (['', '   ', '\t\n'], ['', '', '']),
    ([], []),
])
def test_strip_whitespace(elements: list, expected: list):
    assert strip_whitespace(elements) == expected


@pytest.mark.parametrize('elements, expected', [
    ([1, 2, 2, 3], 2),
    ([1, 1, 2, 2, 3], 1),
    (['a', 'b', 'b', 'c', 'c', 'c'], 'c'),
    ([True, True, False, True], True),
    ([1], 1),
    ([None, 'not none', None, 'not none', None], None)
])
def test_most_frequent(elements: list, expected: Any):
    assert most_frequent(elements) == expected


@pytest.mark.parametrize('elements, expected', [
    (['apple', 'banana', 'cherry'], 'banana'),
    (['a', 'ab', 'abc', 'abcd'], 'abcd'),
    (['same', 'size', 'test'], 'same'),
    ([], None),
    (['one'], 'one'),
    (['long', 'longer', 'longest', 'tiny'], 'longest')
])
def test_longest(elements: list, expected: Any):
    assert longest(elements) == expected


@labeled_tests({
    'all truthy': [
        ([1, 'test', True], [1, 'test', True]),
        ([True, True], [True, True]),
        (['Text'], ['Text'])
    ],
    'all falsy': [
        ([None, False, 0, ''], []),
        ([False, False], []),
        ([0], []),
        ([None], []),
    ],
    'mixed':
        ([0, False, None, '', 1, 'text', True], [1, 'text', True]),
    'empty':
        ([], [])
})
def test_exclude_falsy(elements: list, expected: list):
    assert exclude_falsy(elements) == expected


@labeled_tests({
    'complete match': [
        ('sample', ['sample', 'test', 'content'], 'sample'),
        ('test', ['sample', 'test', 'content'], 'test'),
        ('content', ['sample', 'test', 'content'], 'content')
    ],
    'word match': [
        ('sample', ['sample str', 'test str', 'str content'], 'sample str'),
        ('test', ['sample str', 'test str', 'str content'], 'test str'),
        ('content', ['sample str', 'test str', 'str content'], 'str content'),
    ],
    'partial match': [
        ('s', ['samples', 'testing', 'content'], 'samples'),
        ('test', ['samples', 'testing', 'content'], 'testing'),
        ('tent', ['samples', 'testing', 'content'], 'content'),
    ],
    'multiple matches': [
        ('e', ['sample', 'test', 'content'], 'sample'),
        ('', ['sample', 'test', 'content'], 'sample'),
        ('te', ['sample', 'test', 'content'], 'test'),
        ('content', ['sample content', 'test', 'content'], 'sample content')
    ],
    'no match': [
        ('missing', ['sample', 'test', 'content'], None),
        ('test', [], None)
    ]
})
def test_first_str_with(substring: str, strings: list[str], expected: Optional[str]):
    assert first_str_with(substring, strings) == expected


@labeled_tests({
    'single value': [
        ([1], 1, 1),
        ([True], True, True),
        (['text'], 'text', 'text')
    ],
    'one truthy value':
        ([0, False, 1, None, ''], 1, 1),
    'multiple truthy value': [
        ([1, 2, 3], 1, 3),
        ([True, 23, 'text'], True, 'text')
    ],
    'mixed': [
        ([0, 1, 2, 3, 0], 1, 3),
        ([False, 0, 6, 'text', True, ''], 6, True)
    ],
    'all falsy':
        ([None, False, 0, ''], None, None),
    'empty':
        ([], None, None)
})
def test_first_last(elements: list, expected_first: Any, expected_last: Any):
    assert first(elements) == expected_first
    assert last(elements) == expected_last
