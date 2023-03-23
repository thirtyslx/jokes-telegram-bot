from bot.database.main import Database
from bot.database.models import Jokes


def delete_all_jokes():
    Database().session.query(Jokes).delete(synchronize_session=False)
    Database().session.commit()
