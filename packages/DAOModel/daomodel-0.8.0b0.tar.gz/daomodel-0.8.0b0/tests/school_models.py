from datetime import date
from typing import Optional

import pytest
from sqlalchemy import ForeignKeyConstraint
from sqlmodel import Field

from daomodel import DAOModel
from daomodel.dao import DAO
from daomodel.fields import Identifier, Unsearchable, ReferenceTo
from daomodel.testing import TestDAOFactory
from daomodel.util import next_id


class Person(DAOModel, table=True):
    name: Identifier[str]
    age: Identifier[int]
    ssn: Unsearchable[Optional[str]] = Field(unique=True)


class Book(DAOModel, table=True):
    name: Identifier[str]
    subject: str
    owner: int = ReferenceTo('student.id')


class Hall(DAOModel, table=True):
    location: Identifier[str]
    floor: Identifier[int]
    color: str


class Locker(DAOModel, table=True):
    __table_args__ = (
        ForeignKeyConstraint(
            ['location', 'floor'],
            ['hall.location', 'hall.floor'],
        ),
    )

    number: Identifier[int]
    owner: int = ReferenceTo('student.id')
    location: str
    floor: int


class BasePerson(DAOModel):
    id: Identifier[int]
    name: Optional[str]


class Staff(BasePerson, table=True):
    hire_date: date


class Student(BasePerson, table=True):
    gender: Optional[str]
    active: bool = True

    class Meta:
        searchable_relations = {
            Book.name, Book.subject, Locker.number,
            (Locker, Hall.color)
        }


@pytest.fixture(name='person_dao')
def person_dao_fixture(daos: TestDAOFactory) -> DAO:
    dao = daos[Person]
    dao.create_with(name='John', age=23)
    dao.create_with(name='Joe', age=32)
    dao.create_with(name='Mike', age=25)
    dao.create_with(name='John', age=45)
    dao.create_with(name='Greg', age=31)
    dao.create_with(name='Mike', age=18)
    dao.create_with(name='Paul', age=25)
    return dao


pk_ordered = [
    Person(name='Greg', age=31),
    Person(name='Joe', age=32),
    Person(name='John', age=23),
    Person(name='John', age=45),
    Person(name='Mike', age=18),
    Person(name='Mike', age=25),
    Person(name='Paul', age=25)
]
age_ordered = [
    Person(name='Mike', age=18),
    Person(name='John', age=23),
    Person(name='Mike', age=25),
    Person(name='Paul', age=25),
    Person(name='Greg', age=31),
    Person(name='Joe', age=32),
    Person(name='John', age=45)
]
duplicated_names = [
    Person(name='John', age=23),
    Person(name='John', age=45),
    Person(name='Mike', age=18),
    Person(name='Mike', age=25)
]
unique_names = [
    Person(name='Greg', age=31),
    Person(name='Joe', age=32),
    Person(name='Paul', age=25)
]


def setup_students(daos: TestDAOFactory) -> DAO:
    dao = daos[Student]
    dao.create_with(id=100, name='Bob', gender='m')
    dao.create_with(id=next_id(), name='Mike', gender='m')
    dao.create_with(id=next_id(), name='John', gender='m', active=False)
    dao.create_with(id=next_id(), name='Jerry', gender='m')
    dao.create_with(id=next_id(), name='Carl', gender='m')
    dao.create_with(id=next_id(), name='Barbara', gender='f')
    dao.create_with(id=next_id(), name='Mary', gender='f', active=False)
    dao.create_with(id=next_id(), name='Jill', gender='f', active=False)
    dao.create_with(id=next_id(), name='Jessie', gender='f')
    dao.create_with(id=next_id(), name='Karen', gender='f')
    dao.create_with(id=next_id(), name='Sam')
    dao.create_with(id=next_id(), active=False)
    dao.create(next_id())
    return dao


@pytest.fixture(name='student_dao')
def student_dao_fixture(daos: TestDAOFactory) -> DAO:
    return setup_students(daos)


@pytest.fixture(name='school_dao')
def school_dao_fixture(daos: TestDAOFactory) -> DAO:
    dao = setup_students(daos)
    book_dao = daos[Book]
    book_dao.create_with(name='Biology 101', subject='Science', owner=100)
    book_dao.create_with(name='Art of the World', subject='Art', owner=101)
    book_dao.create_with(name='Pre-Calculus', subject='Math', owner=102)
    book_dao.create_with(name='Calculus', subject='Math', owner=103)
    hall_dao = daos[Hall]
    hall_dao.create_with(location='EAST', floor=1, color='green')
    hall_dao.create_with(location='WEST', floor=1, color='red')
    hall_dao.create_with(location='EAST', floor=2, color='blue')
    hall_dao.create_with(location='WEST', floor=2, color='yellow')
    locker_dao = daos[Locker]
    locker_dao.create_with(number=1101, owner=100, location='EAST', floor=1)
    locker_dao.create_with(number=1102, owner=108, location='EAST', floor=1)
    locker_dao.create_with(number=1103, owner=103, location='EAST', floor=1)
    locker_dao.create_with(number=1104, owner=104, location='WEST', floor=1)
    locker_dao.create_with(number=1105, owner=109, location='WEST', floor=1)
    locker_dao.create_with(number=1106, owner=101, location='WEST', floor=1)
    locker_dao.create_with(number=1201, owner=107, location='EAST', floor=2)
    locker_dao.create_with(number=1202, owner=110, location='EAST', floor=2)
    locker_dao.create_with(number=1203, owner=102, location='EAST', floor=2)
    locker_dao.create_with(number=1204, owner=106, location='WEST', floor=2)
    locker_dao.create_with(number=1205, owner=111, location='WEST', floor=2)
    locker_dao.create_with(number=1206, owner=105, location='WEST', floor=2)
    return dao


def split(to_split: list, target_size: int) -> tuple[list, ...]:
    return tuple(to_split[x:x+target_size] for x in range(0, len(to_split), target_size))


all_students = [
    Student(id=100),
    Student(id=101),
    Student(id=102),
    Student(id=103),
    Student(id=104),
    Student(id=105),
    Student(id=106),
    Student(id=107),
    Student(id=108),
    Student(id=109),
    Student(id=110),
    Student(id=111),
    Student(id=112)
]
active = [
    Student(id=100),
    Student(id=101),
    Student(id=103),
    Student(id=104),
    Student(id=105),
    Student(id=108),
    Student(id=109),
    Student(id=110),
    Student(id=112)
]
inactive = [
    Student(id=102),
    Student(id=106),
    Student(id=107),
    Student(id=111)
]
active_females = [
    Student(id=105),
    Student(id=108),
    Student(id=109)
]
having_gender = [
    Student(id=100),
    Student(id=101),
    Student(id=102),
    Student(id=103),
    Student(id=104),
    Student(id=105),
    Student(id=106),
    Student(id=107),
    Student(id=108),
    Student(id=109)
]
having_book = [
    Student(id=100),
    Student(id=101),
    Student(id=102),
    Student(id=103)
]
having_math_book = [
    Student(id=102),
    Student(id=103)
]
not_having_name = [
    Student(id=111),
    Student(id=112)
]
not_having_locker = [
    Student(id=112)
]
in_blue_hall = [
    Student(id=102),
    Student(id=107),
    Student(id=110)
]
page_one, page_two, page_three = split(all_students, 5)
