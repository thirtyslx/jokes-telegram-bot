from aiogram import Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.types import Message

from bot.filters.main import IsAdmin
from bot.keyboards import ReplyKb
from bot.parser import gather_data
from bot.misc import Config


async def __handle_gather_data(message: Message):
    await message.answer('Started gathering data, please wait...', reply_markup=ReplyKb.get_admin_panel(True))
    await gather_data()
    await message.answer('Gathered data successfully!', reply_markup=ReplyKb.get_admin_panel())


async def __handle_data_gathering_in_progress(message: Message):
    await message.answer('Data gathering in progress. Please, wait...', reply_markup=ReplyKb.get_admin_panel(True))


async def __handle_menu(message: Message):
    await message.answer('Menu', reply_markup=ReplyKb.get_main(Config.RAND_CATEGORY))


async def __cmd_admin_panel(message: Message):
    await message.answer('Admin panel', reply_markup=ReplyKb.get_admin_panel())


def register_admin_handlers(dp: Dispatcher) -> None:
    dp.register_message_handler(__cmd_admin_panel, IsAdmin(), commands=['admin', 'admin_panel'])
    dp.register_message_handler(__handle_gather_data, IsAdmin(), commands='gather_data')
    dp.register_message_handler(__handle_gather_data, IsAdmin(), Text(equals='Обновить базу шуток'))
    dp.register_message_handler(__handle_data_gathering_in_progress, IsAdmin(), Text(equals='Обновление базы...'))
    dp.register_message_handler(__handle_menu, IsAdmin(), Text(equals='Меню'))
