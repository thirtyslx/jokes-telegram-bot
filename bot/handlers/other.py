from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.utils.deep_linking import decode_payload

from bot.database.methods.get import get_categories, get_default_category
from bot.database.methods.insert import create_user
from bot.handlers.user import change_category
from bot.keyboards import ReplyKb
from bot.misc.html_tags import b, u, i, href


async def __cmd_start(message: Message) -> None:
    create_user(message.from_user.id)
    args = decode_payload(message.get_args())
    if args and args.startswith('change-category-'):
        category = args.lstrip('change-category-')
        if category in get_categories():
            await change_category(message, category)
            return
    await __cmd_help(message)


async def __cmd_help(message: Message):
    await message.answer('\n'.join((
        u(b('Помощь')),
        '',
        i('Описание'),
        'Данный телеграм бот был разработан как проект в ходе второго года обучения в Яндекс Лицее.',
        '',
        i('Команды'),
        '/start           - Запустить бота',
        '/help            - Получить это сообщение',
        '/get_joke        - Шутка из текущей категории',
        '/get_random_joke - Шутка из случайной категории',
        '/change_category - Изменить категорию',
        '/list_categories - Список всех доступных категорий',
        '/admin_panel     - Открыть админ панель',
        '/gather_data     - Пересобрать базу шуток',
        '/menu            - Вернуться в главное меню',
        '',
        i('Лицензия'),
        f'Данный бот является свободым ПО и распространяется под лицензией '
        f'{href("https://www.gnu.org/licenses/gpl-3.0.txt", "GPLv3")}. Исходный код:',
        'https://gitlab.com/assbreaker/jokes-telegram-bot',
        '',
        '© Зубарев Григорий, Зубарев Пётр, Фурсов Михаил',
    )), reply_markup=ReplyKb.get_main(get_default_category(message.from_user.id)), disable_web_page_preview=True)


def get_other_commands() -> tuple[tuple[str, str], ...]:
    return (
        ('/start', 'Запустить бота'),
        ('/help', 'Помощь'),
    )


def register_other_handlers(dp: Dispatcher) -> None:
    dp.register_message_handler(__cmd_start, commands='start')
    dp.register_message_handler(__cmd_help, commands='help')
