from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.utils.deep_linking import decode_payload

from bot.database.methods.create import create_user
from bot.database.methods.get import get_categories
from bot.keyboards import ReplyKb
from bot.misc import Config
from bot.handlers.user import change_category


async def __cmd_start(message: Message) -> None:
    create_user(message.from_user.id)
    args = decode_payload(message.get_args())
    if args and args.startswith('change-category-'):
        category = args.lstrip('change-category-')
        if category in get_categories():
            await change_category(message, category)
            return
    await message.answer('Анекдоты',
                         reply_markup=ReplyKb.get_main(Config.RAND_CATEGORY))


async def __help(message: Message):
    await message.answer()


def register_other_handlers(dp: Dispatcher) -> None:
    dp.register_message_handler(__cmd_start, commands='start')
