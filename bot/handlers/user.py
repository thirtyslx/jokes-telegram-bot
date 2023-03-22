from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup
from aiogram.dispatcher.filters import Text
from aiogram.utils.deep_linking import get_start_link

import bot.parser.__main__
from bot.keyboards import ReplyKb, InlineKb
from bot.misc import Config, b, u, code, url
from bot.database.methods.get import get_joke_by_category, get_categories


async def __send_joke(message: Message,
                      joke: str,
                      category: str,
                      top_text: str,
                      keyboard: ReplyKeyboardMarkup,
                      ):
    joke = joke.replace('\n', '\n\n')
    link = await get_start_link(f"change_category {category}", encode=True)
    await message.answer('{} ({})\n\n{}'.format(u(b(top_text)), b(url(link, category)), joke),
                         reply_markup=keyboard)


async def __handle_list_categories(message: Message):
    await message.reply(u(b('Доступные Категории Анекдотов:')),
                        reply_markup=InlineKb.get_list_categories(get_categories()))


async def __handle_change_category(query: CallbackQuery):
    category = query.data.split('set-category-')[-1]
    await query.bot.answer_callback_query(query.id)
    await __cmd_change_category(query.message, category)


async def __handle_random_joke(message: Message):
    if message.text != Config.RAND_BTN:
        category = message.text.replace('(', '').replace(')', '').split('Случайный ')[-1]
    else:
        category = Config.RAND_BTN
    joke, joke_category = get_joke_by_category(category)
    await __send_joke(message=message,
                      joke=joke,
                      category=joke_category,
                      top_text='Случайный Анекдот',
                      keyboard=ReplyKb.get_main(category),
                      )


async def __cmd_change_category(message: Message, category: str = None):
    if not category:
        category = message.get_args()
    if not category:
        await message.answer('\n'.join((u(b('Usage:')),
                                        code("/change_category [category]"),
                                        '',
                                        b('To get list of available categories you can use:'),
                                        code('/list_categories'),
                                        )), reply_markup=ReplyKb.get_main(Config.RAND_CATEGORY))
    else:
        categories = get_categories()
        if category in categories:
            await message.answer(f'Категория изменена на "{u(b(category))}"',
                                 reply_markup=ReplyKb.get_main(category))
        else:
            await message.answer('\n'.join((u(b(f'ERROR: {category}: No such category')),
                                            '',
                                            b('To get list of available categories you can use') + ':',
                                            code('/list_categories'),
                                            )), reply_markup=ReplyKb.get_main(Config.RAND_CATEGORY))


async def __cmd_list_categories(message: Message, categories: tuple[str, str] = get_categories()):
    await message.answer('\n'.join((u(b('Avaliable categories are:')),
                                    *[f'{" " * 8}{c}' for c in categories])),
                         reply_markup=ReplyKb.get_main(Config.RAND_CATEGORY))


async def cmd_scrap(msg: Message):
    await msg.answer('Started gathering data', reply_markup=ReplyKb.get_main(Config.RAND_CATEGORY))
    await bot.parser.__main__.gather_data()
    await msg.answer('Gathered data successfully', reply_markup=ReplyKb.get_main(Config.RAND_CATEGORY))


def register_user_handlers(dp: Dispatcher) -> None:
    dp.register_message_handler(__handle_random_joke, Text(startswith='Случайный'))
    dp.register_message_handler(__handle_list_categories, Text(equals='Изменить Категорию'))
    dp.register_message_handler(__cmd_change_category, commands='change_category')
    dp.register_message_handler(__cmd_list_categories, commands='list_categories')
    dp.register_message_handler(cmd_scrap, commands='scrap')

    dp.register_callback_query_handler(__handle_change_category,
                                       lambda c: c.data and c.data.startswith('set-category-'))
