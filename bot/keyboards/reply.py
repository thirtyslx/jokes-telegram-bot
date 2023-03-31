from abc import ABC

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from bot.misc.config import Config


class ReplyKb(ABC):
    def __new__(cls, *args, **kwargs):
        raise 'I am a static! Dont touch me...'

    @staticmethod
    def get_main(category: str) -> ReplyKeyboardMarkup:
        kb = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        buttons = []
        if category != Config.RAND_CATEGORY and category != Config.RAND_BTN:
            buttons.append(KeyboardButton(text=f'Случайный ({category})'))
        else:
            buttons.append(KeyboardButton(text=Config.RAND_BTN))
        buttons.append(KeyboardButton(text='Изменить Категорию'))
        kb.add(*buttons)
        return kb

    @staticmethod
    def get_admin_panel(collecting_data_now=False):
        kb = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        buttons = []
        if collecting_data_now:
            buttons.append(KeyboardButton(text='Обновление базы...'))
        else:
            buttons.append(KeyboardButton(text='Обновить базу шуток'))
        buttons.append(KeyboardButton(text='Меню'))
        kb.add(*buttons)
        return kb
