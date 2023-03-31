from bot.database.main import Database
from bot.database.models import User


def is_admin(telegram_id: int) -> bool:
    # return bool(1)
    return bool(Database().session.query(User.admin).filter(User.telegram_id == telegram_id).one()[0])
