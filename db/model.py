from sqlalchemy import Column, String, Integer

from db import db
from db.utils import CreatedModel

db.init()


class User(CreatedModel):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    chat_id = Column(String(100))
    fullname = Column(String(255))
    username = Column(String(50))


class Movies(CreatedModel):
    __tablename__ = 'movies'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    path = Column(String(255))
    country = Column(String(100))
    language = Column(String(100))
    date = Column(String(100))
    genre = Column(String(100))
    seen = Column(Integer, default=0)


class Admins(CreatedModel):
    __tablename__ = 'admins'
    id = Column(Integer, primary_key=True)
    chat_id = Column(String(100))
