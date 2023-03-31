from bot.database.main import Database
from bot.database.models import User


def set_default_category(telegram_id: int, category: str) -> None:
    Database().session.query(User).filter(User.telegram_id == telegram_id).update(
        values={User.default_category: category})
    Database().session.commit()
