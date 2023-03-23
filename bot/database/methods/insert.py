from bot.database.main import Database
from bot.database.models import Jokes


async def save_joke(jokes: list[str, str], category: str) -> None:
    for joke in jokes:
        Database().session.add(Jokes(joke=joke, category=category))
    Database().session.commit()
