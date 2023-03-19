from abc import ABC

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from bot.misc.config import Config


# from bot.database.models import User
# from bot.database import get_all_cities_by_order_or_none, get_city_by_abb_or_none, get_all_city_of_user_or_none


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
