from sqlalchemy.orm import declared_attr

import daomodel


class DAOModel(daomodel.DAOModel):
    """A DAOModel configured to act just like an SQLModel."""

    @declared_attr
    def __tablename__(self) -> str:
        return self.__name__.lower()
