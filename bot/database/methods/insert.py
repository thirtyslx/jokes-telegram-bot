from loguru import logger
from sqlalchemy.exc import NoResultFound

from bot.database import Database
from bot.database.models import Joke, User
from bot.misc import Config


async def save_joke(jokes: list[str, str], category: str) -> None:
    session = Database().session
    for joke in jokes:
        try:
            session.query(Joke.joke).filter(Joke.joke == joke).one()
        except NoResultFound:
            session.add(Joke(joke=joke, category=category))
    session.commit()


def create_user(telegram_id: int) -> None:
    session = Database().session
    try:
        session.query(User.telegram_id).filter(User.telegram_id == telegram_id).one()
    except NoResultFound:
        admin = telegram_id in Config.ADMINS
        session.add(User(telegram_id=telegram_id, admin=admin))
        session.commit()
        logger.info(f'Added new {"admin" if admin else "user"}: {telegram_id}')
