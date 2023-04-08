from sqlalchemy.exc import NoResultFound

from bot.database import Database
from bot.database.models import Joke


async def save_joke(jokes: list[str, str], category: str) -> None:
    session = Database().session
    for joke in jokes:
        try:
            session.query(Joke.joke).filter(Joke.joke == joke).one()
        except NoResultFound:
            session.add(Joke(joke=joke, category=category))
    session.commit()
