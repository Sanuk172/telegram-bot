import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase


class Data(SqlAlchemyBase):
    __tablename__ = 'dates'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    date = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    event = sqlalchemy.Column(sqlalchemy.String, nullable=False)
