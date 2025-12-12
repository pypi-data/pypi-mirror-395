from typing import List

from daomodel import DAOModel
from daomodel.fields import Identifier
from daomodel.testing import TestDAOFactory


class Album(DAOModel, table=True):
    id: Identifier[int]
    list: list['Photo']
    List: List['Photo']


class Photo(DAOModel, table=True):
    id: Identifier[int]
    album: Album


def test_implicit_relationship():
    with TestDAOFactory() as daos:
        album_dao = daos[Album]
        photo_dao = daos[Photo]
        album_dao.create(1)
        album_dao.create(2)
        album_dao.create(3)
        photo_dao.create_with(id=1, album=1)
        photo_dao.create_with(id=2, album=3)
        photo_dao.create_with(id=3, album=3)

        album = album_dao.get(1)
        assert album.list == album.List == [photo_dao.get(1)]
        album = album_dao.get(2)
        assert album.list == album.List == []
        album = album_dao.get(3)
        assert album.list == album.List == [photo_dao.get(2), photo_dao.get(3)]
