from loguru import logger

from bot.database.main import Database
from bot.database.models import Joke


def delete_all_jokes():
    Database().session.query(Joke).delete(synchronize_session=False)
    Database().session.commit()
    logger.info('Deleted all jokes from db')
