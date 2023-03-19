from sqlalchemy.sql.expression import func

from bot.database.main import Database
from bot.database.models import Jokes
from bot.misc.config import Config


def get_joke_by_category(category: str) -> tuple[str, str]:
    if category == Config.RAND_BTN:
        joke, category = Database().session.query(Jokes.joke, Jokes.category).order_by(func.random()).first()
    else:
        joke, = Database().session.query(Jokes.joke).filter(Jokes.category == category).order_by(func.random()).first()
    return joke, category


def get_categories() -> tuple[str, str]:
    query = Database().session.query(Jokes.category).distinct().all()
    categories = (Config.RAND_CATEGORY, *[el[0] for el in query])
    return categories
