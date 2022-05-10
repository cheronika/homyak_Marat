import sqlalchemy as sa
from .db_session import SqlAlchemyBase


class Lost(SqlAlchemyBase):
    __tablename__ = 'lost_animals'
    id = sa.Column(sa.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    city = sa.Column(sa.String, nullable=True)
    lost_place = sa.Column(sa.String, nullable=False)
    lost_date = sa.Column(sa.DATE, nullable=True)
    animal = sa.Column(sa.String, nullable=True)
    stamp = sa.Column(sa.BOOLEAN, nullable=True)
    collar = sa.Column(sa.BOOLEAN, nullable=True)
    information = sa.Column(sa.String, nullable=True)
    photo = sa.Column(sa.BLOB, nullable=True)
    owner_phone = sa.Column(sa.String, nullable=True)
    is_find = sa.Column(sa.BOOLEAN, nullable=False)


class Found(SqlAlchemyBase):
    __tablename__ = 'found_animals'
    id = sa.Column(sa.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    city = sa.Column(sa.String, nullable=True)
    found_place = sa.Column(sa.String, nullable=False)
    found_date = sa.Column(sa.DATE, nullable=True)
    animal = sa.Column(sa.String, nullable=True)
    stamp = sa.Column(sa.BOOLEAN, nullable=True)
    collar = sa.Column(sa.BOOLEAN, nullable=True)
    information = sa.Column(sa.String, nullable=True)
    photo = sa.Column(sa.BLOB, nullable=True)
    finder_phone = sa.Column(sa.String, nullable=True)
