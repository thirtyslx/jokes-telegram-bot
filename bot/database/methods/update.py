from loguru import logger

from bot.database import Database
from bot.database.models import User


def set_default_category(telegram_id: int, category: str) -> None:
    session = Database().session
    session.query(User).filter(User.telegram_id == telegram_id).update(
        values={User.default_category: category})
    session.commit()
    logger.info(f"User {telegram_id} changed category to '{category}'")
