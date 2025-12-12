from datetime import date
from typing import Optional, Any

import pytest

from daomodel import DAOModel
from daomodel.change_set import Preference, ChangeSet, MergeSet, Resolved, Unresolved
from daomodel.dao import Conflict
from daomodel.fields import Identifier
from daomodel.list_util import most_frequent
from daomodel.testing import labeled_tests


class CalendarEvent(DAOModel, table=True):
    title: Identifier[str]
    day: date
    time: Optional[str] = 'All Day'
    location: Optional[str]
    description: Optional[str]


dads_entry = CalendarEvent(
    title='Family Picnic',
    day=date(2025, 6, 20),
    time='11:00 AM',
    location='Central Park',
    description='Annual family picnic with games and BBQ.'
)
moms_entry = CalendarEvent(
    title='Family Picnic',
    day=date(2025, 6, 20),
    time='12:00 PM',
    location='Central Park',
    description='Picnic with family and friends, do not forget the salads!'
)
sons_entry = CalendarEvent(
    title='Family Picnic',
    day=date(2025, 6, 19),
    time='12:00 PM',
    description='Bring your football and frisbee!'
)
daughters_entry = CalendarEvent(
    title='Family Picnic',
    day=date(2025, 6, 20),
    time='All Day',
    location='The Park'
)
unrelated_entry = CalendarEvent(
    title='Dentist Appointment',
    day=date(2025, 7, 1)
)


rules = {
    'title': Preference.NOT_APPLICABLE,
    'day': max,
    'time': min,
    'location_conflict': Preference.LEFT,
    'description_conflict': '\n\n'.join
}
merge_rules = {**rules, 'location_conflict': most_frequent, 'description_conflict': Preference.LEFT}


def test_change_set():
    assert 'title' not in ChangeSet(dads_entry, unrelated_entry)


def test_change_set__include_pk():
    assert 'title' in ChangeSet(dads_entry, unrelated_entry, include_pk=True)


def test_get_baseline_get_target():
    change_set = ChangeSet(dads_entry, moms_entry)
    assert change_set.get_baseline('time') == change_set.get_left('time') == '11:00 AM'
    assert change_set.get_target('time') == change_set.get_right('time') == '12:00 PM'


@labeled_tests({
    'ChangeSet has target value':
        (ChangeSet(dads_entry, moms_entry), 'time', True),
    'ChangeSet does not have target value':
        (ChangeSet(dads_entry, sons_entry), 'location', False),
    'Single Target MergeSet has target value':
        (MergeSet(dads_entry, moms_entry), 'time', True),
    'Single Target MergeSet does not have target value':
        (MergeSet(dads_entry, sons_entry), 'location', False),
    'Multiple Target MergeSet has all target value':
        (MergeSet(dads_entry, moms_entry, sons_entry, daughters_entry), 'time', True),
    'Multiple Target MergeSet has some target value':
        (MergeSet(dads_entry, moms_entry, sons_entry, daughters_entry), 'description', True),
    'Multiple Target MergeSet has no target value':
        (MergeSet(dads_entry, sons_entry, unrelated_entry), 'location', False),
})
def test_has_target_value(change_set: ChangeSet, field: str, expected: bool):
    assert change_set.has_target_value(field) is expected


@labeled_tests({
    'ChangeSet':
        (ChangeSet(dads_entry, moms_entry), 'time', ['11:00 AM', '12:00 PM']),
    'ChangeSet None Baseline':
        (ChangeSet(daughters_entry, sons_entry), 'description', [None, 'Bring your football and frisbee!']),
    'Single Target MergeSet':
        (MergeSet(dads_entry, sons_entry), 'day', [date(2025, 6, 20), date(2025, 6, 19)]),
    'Multiple Target MergeSet':
        (MergeSet(dads_entry, moms_entry, daughters_entry), 'time', [
            '11:00 AM',
            '12:00 PM',
            'All Day'
        ]),
    'Multiple Target MergeSet with some unchanged values':
        (MergeSet(dads_entry, moms_entry, daughters_entry), 'location', [
            'Central Park',
            'Central Park',
            'The Park'
        ]),
    'Multiple Target MergeSet with None value':
        (MergeSet(dads_entry, moms_entry, sons_entry, daughters_entry), 'description', [
            'Annual family picnic with games and BBQ.',
            'Picnic with family and friends, do not forget the salads!',
            'Bring your football and frisbee!',
            None
        ]),
    'Multiple Target MergeSet with None Baseline':
        (MergeSet(sons_entry, dads_entry, daughters_entry), 'location', [
            None,
            'Central Park',
            'The Park'
        ]),
    'Multiple Target MergeSet with all target matching':
        (MergeSet(sons_entry, dads_entry, moms_entry, daughters_entry), 'day', [
            date(2025, 6, 19),
            date(2025, 6, 20),
            date(2025, 6, 20),
            date(2025, 6, 20)
        ]),
})
def test_all_values(change_set: ChangeSet, field: str, expected: list[Any]):
    assert change_set.all_values(field) == expected


def test_get_resolution():
    change_set = ChangeSet(dads_entry, moms_entry, **rules)
    change_set.resolve_preferences()
    assert (change_set.get_resolution('description') ==
            'Annual family picnic with games and BBQ.\n\nPicnic with family and friends, do not forget the salads!')
    change_set = ChangeSet(moms_entry, dads_entry, **rules)
    change_set.resolve_preferences()
    assert (change_set.get_resolution('description') ==
            'Picnic with family and friends, do not forget the salads!\n\nAnnual family picnic with games and BBQ.')


def test_get_resolution__unresolved():
    assert ChangeSet(dads_entry, moms_entry).get_resolution('time') == '12:00 PM'
    assert ChangeSet(moms_entry, dads_entry).get_resolution('time') == '11:00 AM'


get_preferred_tests = {
    'left': [
        (dads_entry, sons_entry, 'location', Preference.LEFT),
        (dads_entry, daughters_entry, 'time', Preference.LEFT),
        (dads_entry, daughters_entry, 'description', Preference.LEFT),
        (sons_entry, daughters_entry, 'time', Preference.LEFT),
        (sons_entry, daughters_entry, 'description', Preference.LEFT)
    ],
    'right': [
        (sons_entry, moms_entry, 'location', Preference.RIGHT),
        (daughters_entry, moms_entry, 'time', Preference.RIGHT),
        (daughters_entry, moms_entry, 'description', Preference.RIGHT),
        (sons_entry, daughters_entry, 'location', Preference.RIGHT)
    ],
    'both': [
        (dads_entry, moms_entry, 'time', Preference.BOTH),
        (dads_entry, moms_entry, 'description', Preference.BOTH),
        (moms_entry, sons_entry, 'day', Preference.BOTH)
    ]
}
@labeled_tests(get_preferred_tests)
def test_get_preferred(baseline: CalendarEvent, target: CalendarEvent, field: str, expected: Preference):
    assert ChangeSet(baseline, target).get_preferred(field) == expected


@labeled_tests({
    'resolve by preference': [
        (ChangeSet(dads_entry, daughters_entry, location_conflict=Preference.LEFT), 'location', Preference.LEFT),
        (ChangeSet(dads_entry, daughters_entry, location_conflict=Preference.RIGHT), 'location', Preference.RIGHT),
        (ChangeSet(dads_entry, moms_entry, description_conflict=Preference.NOT_APPLICABLE), 'description', Preference.NOT_APPLICABLE),
        (ChangeSet(dads_entry, moms_entry, description_conflict=Preference.NEITHER), 'description', Preference.NEITHER),
        (MergeSet(dads_entry, daughters_entry, location_conflict=Preference.LEFT), 'location', Preference.LEFT),
        (MergeSet(dads_entry, moms_entry, sons_entry, day_conflict=Preference.RIGHT), 'day', Preference.RIGHT),
        (MergeSet(dads_entry, moms_entry, description_conflict=Preference.NEITHER), 'description', Preference.NEITHER)
    ],
    'resolve by comparison': [
        (ChangeSet(dads_entry, sons_entry, day_conflict=max), 'day', Preference.LEFT),
        (ChangeSet(dads_entry, sons_entry, day_conflict=min), 'day', Preference.RIGHT)
    ],
    'static resolve': [
        (ChangeSet(dads_entry, moms_entry, time_conflict='11:00 AM'), 'time', Preference.LEFT),
        (ChangeSet(dads_entry, moms_entry, time_conflict='12:00 PM'), 'time', Preference.RIGHT),
        (ChangeSet(dads_entry, moms_entry, time_conflict='11:30 AM'), 'time', '11:30 AM'),
        (ChangeSet(dads_entry, moms_entry, time_conflict=None), 'time', None)
    ],
    'none value preferred':
        (MergeSet(dads_entry, sons_entry, daughters_entry, description_conflict=None), 'description', (Preference.RIGHT, 1)),
    'both': [
        (ChangeSet(dads_entry, moms_entry, description_conflict='\n\n'.join), 'description',
         'Annual family picnic with games and BBQ.\n\nPicnic with family and friends, do not forget the salads!'),
        (MergeSet(dads_entry, moms_entry, description_conflict='\n\n'.join), 'description',
         'Annual family picnic with games and BBQ.\n\nPicnic with family and friends, do not forget the salads!'),
        (MergeSet(dads_entry, moms_entry, sons_entry, description_conflict='\n\n'.join), 'description',
         'Annual family picnic with games and BBQ.\n\nPicnic with family and friends, do not forget the salads!\n\nBring your football and frisbee!')
    ],
    'default conflict resolution': [
        (ChangeSet(dads_entry, moms_entry, default_conflict=Preference.LEFT), 'time', Preference.LEFT),
        (MergeSet(dads_entry, moms_entry, default_conflict=Preference.LEFT), 'time', Preference.LEFT),
        (MergeSet(dads_entry, moms_entry, sons_entry, default_conflict=Preference.LEFT), 'time', Preference.LEFT)
    ],
    'MergeSet resolve by comparison': [
        (MergeSet(dads_entry, sons_entry, day_conflict=max), 'day', Preference.LEFT),
        (MergeSet(dads_entry, sons_entry, day_conflict=min), 'day', Preference.RIGHT),
        (MergeSet(dads_entry, moms_entry, sons_entry, daughters_entry, day_conflict=max), 'day', Preference.LEFT),
        (MergeSet(dads_entry, moms_entry, sons_entry, daughters_entry, day_conflict=most_frequent), 'day', Preference.LEFT),
        (MergeSet(dads_entry, moms_entry, sons_entry, daughters_entry, time_conflict=most_frequent), 'time', (Preference.RIGHT, 0))
    ],
    'MergeSet static resolve': [
        (MergeSet(dads_entry, moms_entry, time_conflict='11:00 AM'), 'time', Preference.LEFT),
        (MergeSet(dads_entry, sons_entry, daughters_entry, time_conflict='11:00 AM'), 'time', Preference.LEFT),
        (MergeSet(dads_entry, moms_entry, time_conflict='12:00 PM'), 'time', Preference.RIGHT),
        (MergeSet(dads_entry, moms_entry, daughters_entry, time_conflict='All Day'), 'time', (Preference.RIGHT, 1)),
        (MergeSet(dads_entry, moms_entry, sons_entry, time_conflict='11:30 AM'), 'time', '11:30 AM')
    ],
    'multiple target matches':
        (MergeSet(dads_entry, moms_entry, sons_entry, time_conflict='12:00 PM'), 'time', (Preference.RIGHT, 0)),
    'matches left and right':
        (MergeSet(sons_entry, dads_entry, moms_entry, daughters_entry, time_conflict='12:00 PM'), 'time', Preference.LEFT)
})
def test_resolve_conflict(change_set: ChangeSet, field: str, expected: Preference|tuple[Preference.RIGHT, int]|Any):
    assert change_set.resolve_conflict(field) == expected


def test_resolve_conflict__missing():
    with pytest.raises(Conflict):
        ChangeSet(dads_entry, moms_entry).resolve_conflict('time')


@labeled_tests({
    'dad => mom':
        (dads_entry, moms_entry, {
            'description': (
                    'Annual family picnic with games and BBQ.',
                    Resolved('Picnic with family and friends, do not forget the salads!',
                             'Annual family picnic with games and BBQ.\n\nPicnic with family and friends, do not forget the salads!')
            )
        }),
    'dad => son':
        (dads_entry, sons_entry, {
            'description': (
                    'Annual family picnic with games and BBQ.',
                    Resolved('Bring your football and frisbee!',
                             'Annual family picnic with games and BBQ.\n\nBring your football and frisbee!')
            )
        }),
    'dad => daughter':
        (dads_entry, daughters_entry, {}),
    'mom => dad':
        (moms_entry, dads_entry, {
            'time': ('12:00 PM', '11:00 AM'),
            'description': (
                    'Picnic with family and friends, do not forget the salads!',
                    Resolved('Annual family picnic with games and BBQ.',
                             'Picnic with family and friends, do not forget the salads!\n\nAnnual family picnic with games and BBQ.')
            )
        }),
    'mom => son':
        (moms_entry, sons_entry, {
            'description': (
                    'Picnic with family and friends, do not forget the salads!',
                    Resolved('Bring your football and frisbee!',
                             'Picnic with family and friends, do not forget the salads!\n\nBring your football and frisbee!')
            )
        }),
    'mom => daughter':
        (moms_entry, daughters_entry, {}),
    'son => dad':
        (sons_entry, dads_entry, {
            'day': (date(2025, 6, 19), date(2025, 6, 20)),
            'time': ('12:00 PM', '11:00 AM'),
            'location': (None, 'Central Park'),
            'description': (
                    'Bring your football and frisbee!',
                    Resolved('Annual family picnic with games and BBQ.',
                             'Bring your football and frisbee!\n\nAnnual family picnic with games and BBQ.')
            )
        }),
    'son => mom':
        (sons_entry, moms_entry, {
            'day': (date(2025, 6, 19), date(2025, 6, 20)),
            'location': (None, 'Central Park'),
            'description': (
                    'Bring your football and frisbee!',
                    Resolved('Picnic with family and friends, do not forget the salads!',
                             'Bring your football and frisbee!\n\nPicnic with family and friends, do not forget the salads!')
            )
        }),
    'son => daughter':
        (sons_entry, daughters_entry, {
            'day': (date(2025, 6, 19), date(2025, 6, 20)),
            'location': (None, 'The Park')
        }),
    'daughter => dad':
        (daughters_entry, dads_entry, {
            'time': ('All Day', '11:00 AM'),
            'description': (None, 'Annual family picnic with games and BBQ.')
        }),
    'daughter => mom':
        (daughters_entry, moms_entry, {
            'time': ('All Day', '12:00 PM'),
            'description': (None, 'Picnic with family and friends, do not forget the salads!')
        }),
    'daughter => son':
        (daughters_entry, sons_entry, {
            'time': ('All Day', '12:00 PM'),
            'description': (None, 'Bring your football and frisbee!')
        })
})
def test_resolve_preferences(baseline: CalendarEvent, target: CalendarEvent, expected: dict[str, tuple[Any, Any|Resolved]]):
    change_set = ChangeSet(baseline, target, **rules)
    change_set.resolve_preferences()
    assert change_set == expected


def test_resolve_preferences__unresolved():
    change_set = ChangeSet(dads_entry, unrelated_entry, include_pk=True, **rules)
    change_set.resolve_preferences()
    assert change_set['title'] == ('Family Picnic', Unresolved('Dentist Appointment'))


def test_resolve_preferences__chained():
    assert ChangeSet(moms_entry, dads_entry, **rules).resolve_preferences().get_baseline('time') == '12:00 PM'


def test_resolve_preferences__conflict():
    with pytest.raises(Conflict):
        ChangeSet(dads_entry, moms_entry).resolve_preferences()


@labeled_tests({
    'dad => mom':
        (dads_entry, moms_entry, CalendarEvent(
            title='Family Picnic',
            day=date(2025, 6, 20),
            time='11:00 AM',
            location='Central Park',
            description='Annual family picnic with games and BBQ.\n\nPicnic with family and friends, do not forget the salads!'
        )),
    'dad => son':
        (dads_entry, sons_entry, CalendarEvent(
            title='Family Picnic',
            day=date(2025, 6, 20),
            time='11:00 AM',
            location='Central Park',
            description='Bring your football and frisbee!\n\nAnnual family picnic with games and BBQ.'
        )),
    'dad => daughter':
        (dads_entry, daughters_entry, CalendarEvent(
            title='Family Picnic',
            day=date(2025, 6, 20),
            time='11:00 AM',
            location='Central Park',
            description='Annual family picnic with games and BBQ.'
        )),
    'mom => dad':
        (moms_entry, dads_entry, CalendarEvent(
            title='Family Picnic',
            day=date(2025, 6, 20),
            time='12:00 PM',
            location='Central Park',
            description='Annual family picnic with games and BBQ.\n\nPicnic with family and friends, do not forget the salads!'
        )),
    'mom => son':
        (moms_entry, sons_entry, CalendarEvent(
            title='Family Picnic',
            day=date(2025, 6, 20),
            time='12:00 PM',
            location='Central Park',
            description='Bring your football and frisbee!\n\nPicnic with family and friends, do not forget the salads!'
        )),
    'mom => daughter':
        (moms_entry, daughters_entry, CalendarEvent(
            title='Family Picnic',
            day=date(2025, 6, 20),
            time='12:00 PM',
            location='Central Park',
            description='Picnic with family and friends, do not forget the salads!'
        )),
    'son => dad':
        (sons_entry, dads_entry, CalendarEvent(
            title='Family Picnic',
            day=date(2025, 6, 20),
            time='11:00 AM',
            location='Central Park',
            description='Annual family picnic with games and BBQ.\n\nBring your football and frisbee!'
        )),
    'son => mom':
        (sons_entry, moms_entry, CalendarEvent(
            title='Family Picnic',
            day=date(2025, 6, 20),
            time='12:00 PM',
            location='Central Park',
            description='Picnic with family and friends, do not forget the salads!\n\nBring your football and frisbee!'
        )),
    'son => daughter':
        (sons_entry, daughters_entry, CalendarEvent(
            title='Family Picnic',
            day=date(2025, 6, 20),
            time='12:00 PM',
            location='Central Park',
            description='Bring your football and frisbee!'
        )),
    'daughter => dad':
        (daughters_entry, dads_entry, CalendarEvent(
            title='Family Picnic',
            day=date(2025, 6, 20),
            time='11:00 AM',
            location='Central Park',
            description='Annual family picnic with games and BBQ.'
        )),
    'daughter => mom':
        (daughters_entry, moms_entry, CalendarEvent(
            title='Family Picnic',
            day=date(2025, 6, 20),
            time='12:00 PM',
            location='Central Park',
            description='Picnic with family and friends, do not forget the salads!'
        )),
    'daughter => son':
        (daughters_entry, sons_entry, CalendarEvent(
            title='Family Picnic',
            day=date(2025, 6, 20),
            time='12:00 PM',
            location='Central Park',
            description='Bring your football and frisbee!'
        )),
})
def test_apply(baseline: CalendarEvent, target: CalendarEvent, expected: CalendarEvent):
    change_set = ChangeSet(baseline.model_copy(), target, **rules)
    change_set.resolve_preferences()
    assert change_set.apply() == expected


@labeled_tests({
    'dad <= mom, son, daughter':
        (dads_entry, [moms_entry, sons_entry, daughters_entry], CalendarEvent(
            title='Family Picnic',
            day=date(2025, 6, 20),
            time='11:00 AM',
            location='Central Park',
            description='Annual family picnic with games and BBQ.'
        )),
    'mom <= son, daughter, dad':
        (moms_entry, [sons_entry, daughters_entry, dads_entry], CalendarEvent(
            title='Family Picnic',
            day=date(2025, 6, 20),
            time='11:00 AM',
            location='Central Park',
            description='Picnic with family and friends, do not forget the salads!'
        )),
    'son <= daughter, dad, mom':
        (sons_entry, [daughters_entry, dads_entry, moms_entry], CalendarEvent(
            title='Family Picnic',
            day=date(2025, 6, 20),
            time='11:00 AM',
            location='Central Park',
            description='Bring your football and frisbee!'
        )),
    'daughter <= dad, mom, son':
        (sons_entry, [daughters_entry, dads_entry, moms_entry], CalendarEvent(
            title='Family Picnic',
            day=date(2025, 6, 20),
            time='11:00 AM',
            location='Central Park',
            description='Annual family picnic with games and BBQ.'
        )),
})
def test_apply__merge_set(baseline: CalendarEvent, target: list[CalendarEvent], expected: CalendarEvent):
    change_set = MergeSet(baseline.model_copy(), *target, **merge_rules)
    change_set.resolve_preferences()
    assert change_set.apply() == expected


@labeled_tests({
    '1 other model':
        (dads_entry, [moms_entry], {
            'time': ('11:00 AM', [
                '12:00 PM'
            ]),
            'description': ('Annual family picnic with games and BBQ.', [
                'Picnic with family and friends, do not forget the salads!'
            ])
        }),
    'multiple other models': [
        (dads_entry, [moms_entry, sons_entry], {
            'day': (date(2025, 6, 20), [
                date(2025, 6, 20),
                date(2025, 6, 19)
            ]),
            'time': ('11:00 AM', [
                '12:00 PM',
                '12:00 PM'
            ]),
            'location': ('Central Park', [
                'Central Park',
                None
            ]),
            'description': ('Annual family picnic with games and BBQ.', [
                'Picnic with family and friends, do not forget the salads!',
                'Bring your football and frisbee!'
            ])
        }),
        (dads_entry, [moms_entry, daughters_entry], {
            'time': ('11:00 AM', [
                '12:00 PM',
                'All Day'
            ]),
            'location': ('Central Park', [
                'Central Park',
                'The Park'
            ]),
            'description': ('Annual family picnic with games and BBQ.', [
                'Picnic with family and friends, do not forget the salads!',
                None
            ])
        }),
        (dads_entry, [sons_entry, daughters_entry], {
            'day': (date(2025, 6, 20), [
                date(2025, 6, 19),
                date(2025, 6, 20)
            ]),
            'time': ('11:00 AM', [
                '12:00 PM',
                'All Day',
            ]),
            'location': ('Central Park', [
                None,
                'The Park'
            ]),
            'description': ('Annual family picnic with games and BBQ.', [
                'Bring your football and frisbee!',
                None
            ])
        }),
    ],
    'model order': [
        (dads_entry, [moms_entry, sons_entry, daughters_entry], {
            'day': (date(2025, 6, 20), [
                date(2025, 6, 20),
                date(2025, 6, 19),
                date(2025, 6, 20)
            ]),
            'time': ('11:00 AM', [
                '12:00 PM',
                '12:00 PM',
                'All Day'
            ]),
            'location': ('Central Park', [
                'Central Park',
                None,
                'The Park'
            ]),
            'description': ('Annual family picnic with games and BBQ.', [
                'Picnic with family and friends, do not forget the salads!',
                'Bring your football and frisbee!',
                None
            ])
        }),
        (sons_entry, [daughters_entry, moms_entry, dads_entry], {
            'day': (date(2025, 6, 19), [
                date(2025, 6, 20),
                date(2025, 6, 20),
                date(2025, 6, 20)
            ]),
            'time': ('12:00 PM', [
                'All Day',
                '12:00 PM',
                '11:00 AM'
            ]),
            'location': (None, [
                'The Park',
                'Central Park',
                'Central Park'
            ]),
            'description': ('Bring your football and frisbee!', [
                None,
                'Picnic with family and friends, do not forget the salads!',
                'Annual family picnic with games and BBQ.'
            ])
        }),
        (moms_entry, [dads_entry, daughters_entry, sons_entry], {
            'day': (date(2025, 6, 20), [
                date(2025, 6, 20),
                date(2025, 6, 20),
                date(2025, 6, 19)
            ]),
            'time': ('12:00 PM', [
                '11:00 AM',
                'All Day',
                '12:00 PM'
            ]),
            'location': ('Central Park', [
                'Central Park',
                'The Park',
                None,
            ]),
            'description': ('Picnic with family and friends, do not forget the salads!', [
                'Annual family picnic with games and BBQ.',
                None,
                'Bring your football and frisbee!',
            ])
        }),
        (daughters_entry, [moms_entry, dads_entry, sons_entry], {
            'day': (date(2025, 6, 20), [
                date(2025, 6, 20),
                date(2025, 6, 20),
                date(2025, 6, 19)
            ]),
            'time': ('All Day', [
                '12:00 PM',
                '11:00 AM',
                '12:00 PM'
            ]),
            'location': ('The Park', [
                'Central Park',
                'Central Park',
                None
            ]),
            'description': (None, [
                'Picnic with family and friends, do not forget the salads!',
                'Annual family picnic with games and BBQ.',
                'Bring your football and frisbee!'
            ])
        })
    ]
})
def test_merge_set(baseline: CalendarEvent, others: list[CalendarEvent, ...], expected: dict[str, tuple[Any, list[Any]]]):
    assert MergeSet(baseline, *others) == expected


@labeled_tests(get_preferred_tests)
def test_get_preferred(baseline: CalendarEvent, target: CalendarEvent, field: str, expected: Preference):
    assert MergeSet(baseline, *[target] * 3).get_preferred(field) == expected
