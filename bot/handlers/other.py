from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.utils.deep_linking import decode_payload

from bot.keyboards import ReplyKb
from bot.misc import Config
from bot.handlers.user import change_category


async def __cmd_start(message: Message):
    args = decode_payload(message.get_args())
    if not args:
        await message.answer('Анекдоты',
                             reply_markup=ReplyKb.get_main(Config.RAND_CATEGORY))
    elif args.startswith('change-category-'):
        category = args.lstrip('change-category-')
        await change_category(message, category)


async def __help(message: Message):
    await message.answer()


def register_other_handlers(dp: Dispatcher) -> None:
    dp.register_message_handler(__cmd_start, commands='start')
