import pytest
from sqlalchemy.exc import InvalidRequestError

from daomodel.dao import DAO, NotFound, Conflict, PrimaryKeyConflict
from daomodel.testing import TestDAOFactory
from daomodel.util import MissingInput, InvalidArgumentCount, next_id, UnsupportedFeatureError
from tests.school_models import Student, Person, Book, Hall, Locker


def test_create__single_column(daos: TestDAOFactory):
    dao = daos[Student]
    model = dao.create(100)
    assert model == Student(id=100)
    daos.assert_in_db(Student, 100)


def test_create__multi_column(daos: TestDAOFactory):
    model = daos[Person].create('John', 23)
    assert model == Person(name='John', age=23)
    daos.assert_in_db(Person, 'John', 23)


def test_create__default_fields(daos: TestDAOFactory):
    model = daos[Student].create(100)
    assert model.active
    daos.assert_in_db(Student, 100, active=True)


def test_create__required_fields(daos: TestDAOFactory):
    with pytest.raises(InvalidArgumentCount) as error:
        daos[Person].create('John')
    assert 'Expected 2 values, got 1' in str(error.value.detail)


def test_create__too_many_args(daos: TestDAOFactory):
    with pytest.raises(InvalidArgumentCount) as error:
        daos[Student].create(100, 'extra', 'args')
    assert 'Expected 1 values, got 3' in str(error.value.detail)


def test_create_with(daos: TestDAOFactory):
    model = daos[Student].create_with(id=100, name='Bob', active=False)
    assert model == Student(id=100, name='Bob', active=False)
    daos.assert_in_db(Student, 100, name='Bob', active=False)


def test_create_with__model_arg(daos: TestDAOFactory):
    student = daos[Student].create_with(id=100, name='Bob', active=False)
    daos[Book].create_with(name='Algebra I', subject='Math', owner=student)
    daos.assert_in_db(Book, 'Algebra I', subject='Math', owner=100)


def test_create_with__model_arg__composite_key(daos: TestDAOFactory):
    daos[Student].create_with(id=100, name='Bob', active=False)
    hall = daos[Hall].create_with(location='EAST', floor=1, color='green')
    with pytest.raises(UnsupportedFeatureError):
        daos[Locker].create_with(number=808, owner=100, location=hall, floor=hall)


def test_create_with__no_insert(daos: TestDAOFactory):
    model = daos[Student].create_with(False, id=100)
    assert model == Student(id=100)
    daos.assert_not_in_db(Student, 100)


def test_create_with__no_commit(daos: TestDAOFactory):
    dao = daos[Student]
    dao.start_transaction()
    model = dao.create_with(id=100)
    assert model == Student(id=100)
    daos.assert_not_in_db(Student, 100)


def test_insert(daos: TestDAOFactory):
    daos[Student].insert(Student(id=100))
    daos.assert_in_db(Student, 100)


def test_insert__default_fields(daos: TestDAOFactory):
    model = Student(id=100)
    daos[Student].insert(model)
    assert model.active
    daos.assert_in_db(Student, 100, active=True)


def test_insert__conflict(daos: TestDAOFactory):
    dao = daos[Student]
    dao.insert(Student(id=100))
    daos.assert_in_db(Student, 100)
    with pytest.raises(PrimaryKeyConflict):
        dao.insert(Student(id=100))


def test_insert__unique_constraint_violation(daos: TestDAOFactory):
    dao = daos[Person]
    dao.create_with(name='John', age=23, ssn='123-45-6789')
    with pytest.raises(Conflict):
        dao.create_with(name='Bob', age=32, ssn='123-45-6789')


def test_upsert__new(daos: TestDAOFactory):
    daos[Student].upsert(Student(id=100, name='Bob'))
    daos.assert_in_db(Student, 100, name='Bob')


def test_upsert__existing(daos: TestDAOFactory):
    dao = daos[Student]
    model = dao.create(100)
    model.name = 'Bob'
    daos.assert_in_db(Student, 100, name=None)
    dao.upsert(model)
    daos.assert_in_db(Student, 100, name='Bob')


def test_rename(daos: TestDAOFactory):
    dao = daos[Student]
    model = dao.create(100)
    daos.assert_in_db(Student, 100)
    daos.assert_not_in_db(Student, 200)
    dao.rename(model, 200)
    daos.assert_not_in_db(Student, 100)
    daos.assert_in_db(Student, 200)


def test_rename__multiple_columns(daos: TestDAOFactory):
    dao = daos[Person]
    model = dao.create('Alfred', 51)
    daos.assert_in_db(Person, 'Alfred', 51)
    daos.assert_not_in_db(Person, 'Al', 51)

    dao.rename(model, 'Al', 51)
    daos.assert_not_in_db(Person, 'Alfred', 51)
    daos.assert_in_db(Person, 'Al', 51)

    dao.rename(model, 'Fred', 52)
    daos.assert_not_in_db(Person, 'Al', 51)
    daos.assert_in_db(Person, 'Fred', 52)

    dao.rename(model, 'Fred', 53)
    daos.assert_not_in_db(Person, 'Fred', 52)
    daos.assert_in_db(Person, 'Fred', 53)


def test_rename__keep_property_values(daos: TestDAOFactory):
    dao = daos[Student]
    model = dao.create_with(id=100, name='Bob', gender='m', active=False)
    daos.assert_in_db(Student, 100, name='Bob', gender='m', active=False)
    daos.assert_not_in_db(Student, 200)
    dao.rename(model, 200)
    daos.assert_not_in_db(Student, 100)
    daos.assert_in_db(Student, 200, name='Bob', gender='m', active=False)


def test_rename__cascade_foreign_reference(daos: TestDAOFactory):
    student_dao = daos[Student]
    model = student_dao.create(100)
    daos[Book].create_with(name='Algebra I', subject='Math', owner=100)
    daos.assert_in_db(Book, 'Algebra I', subject='Math', owner=100)
    student_dao.rename(model, 200)
    daos.assert_in_db(Book, 'Algebra I', subject='Math', owner=200)


def test_rename__keep_foreign_key(daos: TestDAOFactory):
    daos[Student].create(100)
    book_dao = daos[Book]
    book = book_dao.create_with(name='Algebra I', subject='Math', owner=100)
    daos.assert_in_db(Book, 'Algebra I', subject='Math', owner=100)
    daos.assert_not_in_db(Book, 'Algebra II')
    book_dao.rename(book, 'Algebra II')
    daos.assert_not_in_db(Book, 'Algebra I')
    daos.assert_in_db(Book, 'Algebra II', subject='Math', owner=100)


def test_rename__already_exists(daos: TestDAOFactory):
    dao = daos[Student]
    model = dao.create(100)
    dao.create(200)
    daos.assert_in_db(Student, 100)
    daos.assert_in_db(Student, 200)
    with pytest.raises(PrimaryKeyConflict):
        dao.rename(model, 200)


def test_exists__true(daos: TestDAOFactory):
    dao = daos[Student]
    model = dao.create(100)
    assert dao.exists(model)


def test_exists__false(daos: TestDAOFactory):
    dao = daos[Student]
    model = dao.create_with(id=100, insert=False)
    assert not dao.exists(model)


def test_get__single_column(daos: TestDAOFactory):
    dao = daos[Student]
    dao.create_with(id=100, name='Bob')
    with daos.session_factory() as fresh_session:
        model = DAO(Student, fresh_session).get(100)
        assert model.id == 100
        assert model.name == 'Bob'


def test_get__multiple_column(daos: TestDAOFactory):
    dao = daos[Person]
    dao.create_with(name='John', age=23)
    with daos.session_factory() as fresh_session:
        model = DAO(Person, fresh_session).get('John', 23)
        assert model.name == 'John'
        assert model.age == 23


def test_get__missing_column(daos: TestDAOFactory):
    with pytest.raises(InvalidArgumentCount) as error:
        daos[Person].get('John')
    assert 'Expected 2 values, got 1' in str(error.value.detail)


def test_get__too_many_args(daos: TestDAOFactory):
    with pytest.raises(InvalidArgumentCount) as error:
        daos[Student].get(100, 'extra', 'args')
    assert 'Expected 1 values, got 3' in str(error.value.detail)


def test_get__not_found(daos: TestDAOFactory):
    with pytest.raises(NotFound):
        daos[Student].get(100)


def test_get_with(daos: TestDAOFactory):
    dao = daos[Student]
    dao.create_with(id=100, name='Bob')
    with daos.session_factory() as fresh_session:
        model = DAO(Student, fresh_session).get_with(id=100, name='Mike')
        assert model.id == 100
        assert model.name == 'Mike'


def test_get_with__no_additional_data(daos: TestDAOFactory):
    dao = daos[Student]
    dao.create_with(id=100, name='Bob')
    with daos.session_factory() as fresh_session:
        model = DAO(Student, fresh_session).get_with(id=100)
        assert model.id == 100
        assert model.name == 'Bob'


def test_get_with__blank_data(daos: TestDAOFactory):
    dao = daos[Student]
    dao.create_with(id=100, name='Bob')
    with daos.session_factory() as fresh_session:
        model = DAO(Student, fresh_session).get_with(id=100, name=None)
        assert model.id == 100
        assert model.name is None


def test_get__missing_data(daos: TestDAOFactory):
    with pytest.raises(MissingInput):
        daos[Person].get_with(name='John')


def test_get_with__not_found(daos: TestDAOFactory):
    with pytest.raises(NotFound):
        daos[Student].get_with(id=100, name='Mike')


def test_remove(daos: TestDAOFactory):
    dao = daos[Student]
    model = dao.create(100)
    daos.assert_in_db(Student, 100)
    dao.remove(model)
    daos.assert_not_in_db(Student, 100)


def test_remove__not_found(daos: TestDAOFactory):
    with pytest.raises(NotFound):
        daos[Student].remove(Student(id=100))


def test_commit(daos: TestDAOFactory):
    dao = daos[Student]
    model = dao.create(100)
    model.active = False
    daos.assert_in_db(Student, 100, active=True)
    dao.commit()
    daos.assert_in_db(Student, 100, active=False)


def test_commit__refresh(daos: TestDAOFactory):
    dao = daos[Student]
    dao.create(100)
    dao.start_transaction()
    model = dao.create_with(id=next_id())
    dao.commit(model)
    assert model.id is 101


def test_commit__missing(daos: TestDAOFactory):
    dao = daos[Student]
    model = dao.create(100)
    dao.start_transaction()
    dao.remove(model)
    with pytest.raises(InvalidRequestError):
        dao.commit(model)


def test_transaction(daos: TestDAOFactory):
    dao = daos[Student]
    dao.start_transaction()
    dao.create_with(id=100, name='Billy')
    dao.create_with(id=101, name='Bob')

    dao.commit()
    daos.assert_in_db(Student, 100, name='Billy')
    daos.assert_in_db(Student, 101, name='Bob')


def test_transaction__rollback(daos: TestDAOFactory):
    dao = daos[Student]
    dao.start_transaction()
    dao.create_with(id=100, name='Billy')
    dao.rollback()
    daos.assert_not_in_db(Student, 100)

    dao.create_with(id=101, name='Bob')
    dao.commit()
    daos.assert_in_db(Student, 101, name='Bob')
    daos.assert_not_in_db(Student, 100)


def transaction_setup(daos: TestDAOFactory) -> tuple[DAO, DAO]:
    student_dao = daos[Student]
    book_dao = daos[Book]

    student_dao.start_transaction()

    student_dao.create_with(id=103, name='Charlene')
    student_dao.db.flush()
    book_dao.create_with(name='Physics', subject='Science', owner=103)

    return student_dao, book_dao


def test_transaction__multiple_daos(daos: TestDAOFactory):
    student_dao, book_dao = transaction_setup(daos)

    book_dao.commit()

    daos.assert_in_db(Student, 103, name='Charlene')
    daos.assert_in_db(Book, 'Physics', subject='Science', owner=103)


def test_transaction__multiple_daos__rollback(daos: TestDAOFactory):
    student_dao, book_dao = transaction_setup(daos)

    student_dao.rollback()
    book_dao.commit()  # There is no longer anything to commit

    daos.assert_not_in_db(Student, 103)
    daos.assert_not_in_db(Book, 'Physics')


def test_transaction__multiple_daos__error(daos: TestDAOFactory):
    student_dao, book_dao = transaction_setup(daos)

    try:
        student_dao.create_with(id=103, name='Duplicate')
        student_dao.commit()
    except Conflict:
        student_dao.rollback()

    book_dao.commit()  # There is no longer anything to commit

    daos.assert_not_in_db(Student, 103)
    daos.assert_not_in_db(Book, 'Physics')


def test_transaction__multiple_sessions(daos: TestDAOFactory):
    pytest.skip("This test does not work with in-memory database")


def test_check_pk_arguments__single_column(daos: TestDAOFactory):
    dao = daos[Student]
    result = dao._check_pk_arguments((100,))
    assert result == {'id': 100}


def test_check_pk_arguments__multi_column(daos: TestDAOFactory):
    dao = daos[Person]
    result = dao._check_pk_arguments(('John', 23))
    assert result == {'name': 'John', 'age': 23}


def test_check_pk_arguments__too_few_args(daos: TestDAOFactory):
    dao = daos[Student]
    with pytest.raises(InvalidArgumentCount) as error:
        dao._check_pk_arguments(())
    assert 'Expected 1 values, got 0' in str(error.value.detail)
    assert 'Student primary key' in str(error.value.detail)


def test_check_pk_arguments__too_many_args(daos: TestDAOFactory):
    dao = daos[Student]
    with pytest.raises(InvalidArgumentCount) as error:
        dao._check_pk_arguments((100, 'extra', 'args'))
    assert 'Expected 1 values, got 3' in str(error.value.detail)
    assert 'Student primary key' in str(error.value.detail)
