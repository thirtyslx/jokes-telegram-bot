import sqlalchemy.exc

from bot.database import Database
from bot.database.models import User
from bot.misc import Config


def create_user(telegram_id: int) -> None:
    session = Database().session
    try:
        session.query(User.telegram_id).filter(User.telegram_id == telegram_id).one()
    except sqlalchemy.exc.NoResultFound:
        session.add(User(telegram_id=telegram_id, admin=telegram_id in Config.ADMINS))
        session.commit()
