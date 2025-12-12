from datetime import date

import pytest

from daomodel.base_service import SingleModelService, SOURCE_VALUE, DESTINATION_VALUE, BaseService
from daomodel.list_util import longest
from daomodel.testing import TestDAOFactory
from tests.school_models import Staff, Student, Book


def setup_staff(daos: TestDAOFactory) -> tuple[Staff, Staff]:
    dao = daos[Staff]
    ed = dao.create_with(id=1, name='Ed', hire_date=date(2023, 6, 15))
    edward = dao.create_with(id=2, name='Edward', hire_date=date(2024, 8, 20))
    return ed, edward


def test_merge(daos: TestDAOFactory):
    ed, edward = setup_staff(daos)
    SingleModelService(daos, Staff).merge(ed, 2, name=longest, hire_date=min)
    daos.assert_in_db(Staff, 2, name='Edward', hire_date=date(2023, 6, 15))
    daos.assert_not_in_db(Staff, 1)


def test_merge__source_destination_values(daos: TestDAOFactory):
    ed, edward = setup_staff(daos)
    service = SingleModelService(daos, Staff)
    service.merge(edward, 1, name=DESTINATION_VALUE, hire_date=SOURCE_VALUE)
    daos.assert_in_db(Staff, 1, name='Ed', hire_date=date(2024, 8, 20))
    daos.assert_not_in_db(Staff, 2)


def test_merge__mismatched_model_type(daos: TestDAOFactory):
    setup_staff(daos)
    service = SingleModelService(daos, Staff)
    student = daos[Student].create_with(id=100, name='Student', gender='m')

    with pytest.raises(TypeError):
        service.merge(student, 1)


def test_merge__redirect(daos: TestDAOFactory):
    dao = daos[Student]
    tim = dao.create_with(id=1, name='Tim')
    timothy = dao.create_with(id=2, name='Timothy')
    daos[Book].create_with(name='Biology 101', subject='Science', owner=tim.id)

    SingleModelService(daos, Student).merge(tim, 2, name=longest)
    daos.assert_in_db(Book, 'Biology 101', subject='Science', owner=timothy.id)


def test_dao(daos: TestDAOFactory):
    service = SingleModelService(daos, Staff)
    staff = service.dao.create_with(id=3, name='Alice', hire_date=date(2023, 1, 15))

    daos.assert_in_db(Staff, 3, name='Alice', hire_date=date(2023, 1, 15))

    staff.name = 'Alicia'
    service.dao.commit(staff)

    daos.assert_in_db(Staff, 3, name='Alicia', hire_date=date(2023, 1, 15))


def test_bulk_update(daos: TestDAOFactory):
    service = SingleModelService(daos, Student)
    fee = service.dao.create_with(id=1, name='Fee')
    fi = service.dao.create_with(id=2, name='Fi')
    fo = service.dao.create_with(id=3, name='Fo')
    fum = service.dao.create_with(id=4, name='Fum')

    daos.assert_in_db(Student, 1, name='Fee', active=True)
    daos.assert_in_db(Student, 2, name='Fi', active=True)
    daos.assert_in_db(Student, 3, name='Fo', active=True)
    daos.assert_in_db(Student, 4, name='Fum', active=True)

    service.bulk_update([fee, fi, fo, fum], active=False)

    daos.assert_in_db(Student, 1, name='Fee', active=False)
    daos.assert_in_db(Student, 2, name='Fi', active=False)
    daos.assert_in_db(Student, 3, name='Fo', active=False)
    daos.assert_in_db(Student, 4, name='Fum', active=False)


def test_bulk_update__multiple_fields(daos: TestDAOFactory):
    dao = daos[Student]
    tim = dao.create_with(id=1, name='Tim')
    tom = dao.create_with(id=2, name='Tom')
    tam = dao.create_with(id=3, name='Tam', gender='f')

    BaseService(daos).bulk_update([tim, tom], gender='m', active=False)

    daos.assert_in_db(Student, 1, name='Tim', gender='m', active=False)
    daos.assert_in_db(Student, 2, name='Tom', gender='m', active=False)
    daos.assert_in_db(Student, 3, name='Tam', gender='f', active=True)


def test_bulk_update__multiple_models(daos: TestDAOFactory):
    staff = daos[Staff].create_with(id=1, name='Mr. Staff', hire_date=date(2020, 2, 20))
    student = daos[Student].create_with(id=2, name='Ms. Student')

    BaseService(daos).bulk_update([staff, student], name='Pending Removal')

    daos.assert_in_db(Staff, 1, name='Pending Removal')
    daos.assert_in_db(Student, 2, name='Pending Removal')


def test_bulk_update__empty(daos: TestDAOFactory):
    service = SingleModelService(daos, Staff)
    service.bulk_update([], name='Should not be applied')


def test_bulk_update__non_applicable_fields(daos: TestDAOFactory):
    staff1 = daos[Staff].create_with(id=1, name='Mr. Staff', hire_date=date(2020, 2, 20))
    student1 = daos[Student].create_with(id=2, name='Ms. Student')
    staff2 = daos[Staff].create_with(id=3, name='Sir Staff', hire_date=date(2024, 2, 20))
    student2 = daos[Student].create_with(id=4, name='Mr. Student')

    BaseService(daos).bulk_update(
        [staff1, staff2, student1, student2],
        active=False,
        hire_date=date(2024, 2, 20)
    )

    daos.assert_in_db(Staff, 1, hire_date=date(2024, 2, 20))
    daos.assert_in_db(Staff, 3, hire_date=date(2024, 2, 20))
    daos.assert_in_db(Student, 2, active=False)
    daos.assert_in_db(Student, 4, active=False)


def test_bulk_update__rollback(daos: TestDAOFactory):
    staff1 = daos[Staff].create_with(id=1, name='Mr. Staff', hire_date=date(2020, 2, 20))
    staff2 = daos[Staff].create_with(id=3, name='Sir Staff', hire_date=date(2024, 2, 20))

    with pytest.raises(Exception):
        BaseService(daos).bulk_update(
            [staff1, staff2],
            hire_date='Feb. 20th'
        )

    daos.assert_in_db(Staff, 1, hire_date=date(2020, 2, 20))
    daos.assert_in_db(Staff, 3, hire_date=date(2024, 2, 20))

