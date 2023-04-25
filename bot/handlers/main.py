from aiogram import Dispatcher
from aiogram.types import BotCommand

from bot.handlers.admin import register_admin_handlers, get_admin_commands
from bot.handlers.user import register_user_handlers, get_user_commands
from bot.handlers.other import register_other_handlers, get_other_commands


async def register_all_commands(dp: Dispatcher) -> None:
    commands = (
        *get_admin_commands(dp),
        *get_user_commands(dp),
        *get_other_commands(dp),
    )
    await dp.bot.set_my_commands([BotCommand(*command) for command in commands])


def register_all_handlers(dp: Dispatcher) -> None:
    handlers = (
        register_admin_handlers,
        register_user_handlers,
        register_other_handlers,
    )
    for handler in handlers:
        handler(dp)
