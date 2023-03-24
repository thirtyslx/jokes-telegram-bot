from abc import ABC

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class InlineKb(ABC):
    def __new__(cls, *args, **kwargs):
        raise 'I am a static! Dont touch me...'

    @staticmethod
    def get_list_categories(categories: tuple[str, str]) -> InlineKeyboardMarkup:
        kb = InlineKeyboardMarkup(row_width=2)
        buttons = []
        for c in categories:
            buttons.append(InlineKeyboardButton(text=c, callback_data=f'change-category-{c}'))
        kb.add(*buttons)
        return kb
