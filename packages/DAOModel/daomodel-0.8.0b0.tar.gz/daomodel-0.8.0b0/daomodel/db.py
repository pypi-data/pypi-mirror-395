from typing import Optional

import sqlalchemy
from sqlalchemy import Engine, event
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

from daomodel import DAOModel
from daomodel.dao import DAO
from daomodel.transaction import TransactionMixin


def create_engine(path: Optional[str] = None) -> Engine:
    """Creates an SQLite Engine.

    :param path: the path to the DB file or None to keep the DB in-memory
    :return: The newly created SQLite Engine
    """
    if path is None:
        path = ''
        pool = sqlalchemy.StaticPool
    else:
        path = '/' + path
        pool = None
    return sqlalchemy.create_engine(
        'sqlite://' + path,
        connect_args={'check_same_thread': False},
        poolclass=pool
    )


@event.listens_for(Engine, 'connect')
def enforce_fk_constraints_for_sqlite(connection, _connection_record) -> None:
    cursor = connection.cursor()
    cursor.execute('pragma foreign_keys=on')
    cursor.close()


def init_db(engine: Engine) -> None:
    """Initiates DB tables of all imported SQL/DAOModels

    :param engine: The Engine for which to initialize the DB
    """
    SQLModel.metadata.create_all(engine)


class DAOFactory(TransactionMixin):
    """A Factory for creating DAOs for DAOModels.

    All DAOs/Sessions are auto closed when opened using a `with` statement.
    """
    def __init__(self, session_factory: sessionmaker):
        self.session_factory = session_factory

    def __enter__(self) -> 'DAOFactory':
        self.db = self.session_factory()
        return self

    def __getitem__(self, model: type[DAOModel]) -> DAO:
        return DAO(model, self.db)

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.db.close()
