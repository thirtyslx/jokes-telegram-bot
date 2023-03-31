from bot.database import Database
from bot.database.models import Joke


async def save_joke(jokes: list[str, str], category: str) -> None:
    for joke in jokes:
        Database().session.add(Joke(joke=joke, category=category))
    Database().session.commit()
