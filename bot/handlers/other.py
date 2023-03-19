from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.utils.deep_linking import decode_payload

from bot.keyboards import ReplyKb
from bot.misc import Config
from bot.handlers.user import __cmd_change_category


async def __start(message: Message):
    args = decode_payload(message.get_args())
    if args.startswith('change_category '):
        print(args)
        category = args.split('change_category ')[-1]
        print(category)
        await __cmd_change_category(message, category)
    else:
        await message.answer('Анекдоты',
                             reply_markup=ReplyKb.get_main(Config.RAND_CATEGORY))


async def __help(message: Message):
    await message.answer()


def register_other_handlers(dp: Dispatcher) -> None:
    dp.register_message_handler(__start, commands='start')
