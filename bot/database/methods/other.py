from sqlalchemy.exc import NoResultFound

from bot.database import Database
from bot.database.models import User


def is_admin(telegram_id: int) -> bool:
    try:
        return bool(Database().session.query(User.admin).filter(User.telegram_id == telegram_id).one()[0])
    except NoResultFound:
        return False
