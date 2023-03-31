from sqlalchemy.sql.expression import func

from bot.database.main import Database
from bot.database.models import User, Joke
from bot.misc.config import Config


def get_joke_by_category(category: str) -> tuple[str, str]:
    if category == Config.RAND_BTN:
        joke, category = Database().session.query(Joke.joke, Joke.category).order_by(func.random()).first()
    else:
        joke, = Database().session.query(Joke.joke).filter(Joke.category == category).order_by(func.random()).first()
    return joke, category


def get_categories() -> tuple[str, str]:
    query = Database().session.query(Joke.category).distinct().all()
    categories = (Config.RAND_CATEGORY, *[el[0] for el in query])
    return categories


def get_default_category(telegram_id: int) -> str:
    return Database().session.query(User.default_category).filter(User.telegram_id == telegram_id).one()[0]
