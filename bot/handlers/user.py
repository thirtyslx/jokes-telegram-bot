from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters import Text
from aiogram.utils.deep_linking import get_start_link

from bot.database.methods.get import get_joke_by_category, get_categories
from bot.keyboards import ReplyKb, InlineKb
from bot.misc import Config, b, u, code, url
from bot.parser import gather_data


async def change_category(message: Message, category: str):
    await message.answer(b(f'Категория изменена на "{code(category)}"'),
                         reply_markup=ReplyKb.get_main(category))


async def __send_joke(message: Message, joke: str,
                      category: str, top_text: str):
    joke = joke.replace('\n', '\n\n')
    link = await get_start_link(f'change-category-{category}', encode=True)
    await message.answer(f'{u(b(top_text))} ({b(url(link, category))})\n\n{joke}',
                         reply_markup=ReplyKb.get_main(category))


async def __handle_random_joke(message: Message):
    if message.text == Config.RAND_BTN:
        category = Config.RAND_BTN
    else:
        category = message.text.replace('(', '').replace(')', '').lstrip('Случайный ')
    joke, joke_category = get_joke_by_category(category)
    await __send_joke(message=message, joke=joke,
                      category=joke_category, top_text='Случайный Анекдот')


async def __handle_change_category(query: CallbackQuery):
    category = query.data.lstrip('change-category-')
    await query.bot.answer_callback_query(query.id)
    await change_category(query.message, category)


async def __handle_list_categories(message: Message):
    await message.reply(u(b('Доступные Категории Анекдотов:')),
                        reply_markup=InlineKb.get_list_categories(get_categories()))


async def __cmd_change_category(message: Message):
    category = message.get_args()
    if category in get_categories():
        await change_category(message, category)
    elif category:
        await message.answer('\n'.join((b(f'Error: {code(category)}: No such category'),
                                        '',
                                        b('To get list of available categories you can use:'),
                                        code('/list_categories'))),
                             reply_markup=ReplyKb.get_main(Config.RAND_CATEGORY))
    else:
        await message.answer('\n'.join((u(b('Usage:')),
                                        code("/change_category [category]"),
                                        '',
                                        b('To get list of available categories you can use:'),
                                        code('/list_categories'))),
                             reply_markup=ReplyKb.get_main(Config.RAND_CATEGORY))


async def __cmd_list_categories(message: Message):
    await message.answer('\n'.join((u(b('Available categories are:')),
                                    *[f'{" " * 8}{c}' for c in get_categories()])),
                         reply_markup=ReplyKb.get_main(Config.RAND_CATEGORY))


async def __cmd_parse(msg: Message):
    await msg.answer('Started gathering data, please wait...', reply_markup=ReplyKb.get_main(Config.RAND_CATEGORY))
    await gather_data()
    await msg.answer('Gathered data successfully!', reply_markup=ReplyKb.get_main(Config.RAND_CATEGORY))


def register_user_handlers(dp: Dispatcher) -> None:
    dp.register_message_handler(__handle_random_joke, Text(startswith='Случайный'))
    dp.register_message_handler(__handle_list_categories, Text(equals='Изменить Категорию'))
    dp.register_message_handler(__cmd_change_category, commands=['change_category', 'cc'])
    dp.register_message_handler(__cmd_list_categories, commands=['list_categories', 'lc'])
    dp.register_message_handler(__cmd_parse, commands='parse')

    dp.register_callback_query_handler(__handle_change_category,
                                       lambda c: c.data and c.data.startswith('change-category-'))
