from daomodel import all_models
from daomodel.db import create_engine, init_db
from tests.school_models import *


@pytest.mark.xfail(reason='Fails unless run individually (to better control loaded models)')
def test_all_models():
    engine = create_engine()
    init_db(engine)
    expected = {Person, Book, Hall, Locker, Staff, Student}
    assert all_models(engine) == expected
    connection = engine.connect()
    assert all_models(connection) == expected
