from loguru import logger

from bot.database import Database
from bot.database.models import Joke


def delete_all_jokes():
    session = Database().session
    session.query(Joke).delete(synchronize_session=False)
    session.commit()
    logger.info('Deleted all jokes from database')
