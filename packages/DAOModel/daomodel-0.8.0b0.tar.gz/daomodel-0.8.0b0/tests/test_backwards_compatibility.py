from typing import Optional

from sqlmodel import Field, Relationship

from daomodel.backwards_compatibility import DAOModel
from daomodel.testing import TestDAOFactory


class ParentModel(DAOModel, table=True):
    id: int = Field(primary_key=True)
    children: list['ChildModel'] = Relationship(back_populates='parent')
    _private: list[str]


class ChildModel(DAOModel, table=True):
    id: int = Field(primary_key=True)
    sibling: Optional[int] = Field(foreign_key='childmodel.id', ondelete='SET NULL')
    parent_id: Optional[int] = Field(foreign_key='parentmodel.id')
    parent: Optional['ParentModel'] = Relationship(back_populates='children')


def test_table_naming() -> None:
    assert ParentModel.__table__.name == 'parentmodel'
    assert ChildModel.__table__.name == 'childmodel'


def test_relationship_behavior(daos: TestDAOFactory) -> None:
    parent_dao = daos[ParentModel]
    child_dao = daos[ChildModel]
    parent = parent_dao.create(0)
    child = child_dao.create_with(id=1, parent=parent.id)
    child_dao.create_with(id=2, sibling=1)

    daos.assert_in_db(ChildModel, 2, sibling=1)
    child_dao.remove(child)
    daos.assert_in_db(ChildModel, 2, sibling=None)
