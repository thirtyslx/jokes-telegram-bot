from aiogram.dispatcher.filters import Filter
from aiogram.types import Message

from bot.database.methods.other import is_admin


class IsAdmin(Filter):
    key = 'is_admin'

    async def check(self, message: Message) -> bool:
        return is_admin(telegram_id=message.from_user.id)
