from sqlalchemy import Column, Integer, String

from .main import Database
from bot.misc.config import Config


class Users(Database.BASE):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False, unique=True)
    name = Column(String, nullable=True)
    default_category = Column(String, default=Config.RAND_CATEGORY)


class Jokes(Database.BASE):
    __tablename__ = 'jokes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    joke = Column(String, nullable=False, unique=True)
    category = Column(String, nullable=False)


def register_models() -> None:
    Database.BASE.metadata.create_all(Database().engine)
