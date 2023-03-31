from sqlalchemy import Column, Integer, String

from .main import Database
from bot.misc.config import Config


class User(Database.BASE):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(Integer, nullable=False, unique=True)
    admin = Column(Integer, default=0)
    default_category = Column(String, default=Config.RAND_CATEGORY)


class Joke(Database.BASE):
    __tablename__ = 'jokes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    joke = Column(String, nullable=False, unique=True)
    category = Column(String, nullable=False)


def register_models() -> None:
    Database.BASE.metadata.create_all(Database().engine)
