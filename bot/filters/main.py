from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.dispatcher.filters import Filter

from bot.database.methods.get import is_admin


class IsAdmin(Filter):
    key = 'is_admin'

    async def check(self, message: Message) -> bool:
        return is_admin(telegram_id=message.from_user.id)


def register_all_filters(dp: Dispatcher):
    dp.bind_filter(IsAdmin)
