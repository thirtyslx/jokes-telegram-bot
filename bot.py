import aiosqlite
import asyncio
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.utils.markdown import hbold, hcode, hunderline

from config import BOT_TOKEN, RANDOM_CATEGORY_LABEL
from bot_functions import get_random_joke, get_categories, get_joke_from_category, change_default_category, get_default_category

bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


@dp.message_handler(commands='start')
async def start(message: types.Message):
    start_buttons = ['Случайный', 'Изменить Категорию']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    await message.answer('Анекдоты', reply_markup=keyboard)
    await change_default_category(message.from_user.id, RANDOM_CATEGORY_LABEL, is_new_user=True)


async def send_joke(
        chat_id: int,
        joke: str,
        category: str,
        top_text: str = 'Анекдот',
        keyboard: types.ReplyKeyboardMarkup = None,
):
    joke = joke.replace('\n', '\n\n')
    await bot.send_message(chat_id, f'{hbold(top_text)} ({hunderline(category)}):\n\n{joke}', reply_markup=keyboard)
    # await message.answer(f'{hbold(top_text)} ({hunderline(category)}):\n\n{joke}', reply_markup=keyboard)


@dp.message_handler(Text(startswith='Случайный'))
async def random_joke(message: types.Message):
    # print(f'Случайный ({await get_default_category(message.from_user.id)})', 'Изменить Категорию')
    if (category := await get_default_category(message.from_user.id)) != RANDOM_CATEGORY_LABEL:
        joke = await get_joke_from_category(category)
        start_buttons = [f'Случайный ({category})', 'Изменить Категорию']
    else:
        joke, category = await get_random_joke()
        start_buttons = ['Случайный', 'Изменить Категорию']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    await get_default_category(message.from_user.id)
    # joke = joke.replace('\n', '\n\n')
    await send_joke(
        chat_id=message.from_user.id,
        joke=joke,
        category=category,
        top_text='Случайный Анекдот',
        keyboard=keyboard,
    )
    # await message.answer(f'{hbold("Случайный анекдот")} ({hunderline(category)}):\n\n{joke}', reply_markup=keyboard)


@dp.message_handler(Text(equals='Изменить Категорию'))
async def categories(message: types.Message):
    category_buttons = await get_categories()
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*[types.InlineKeyboardButton(el, callback_data=f'category {el}') for el in category_buttons])
    await message.reply('Доступные Категоии Анекдотов:', reply_markup=keyboard)


@dp.callback_query_handler(lambda c: c.data == 'cat1')
async def process_callback_cat1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Нажата первая кнопка!')


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('category'))
async def process_category_callback(callback_query: types.CallbackQuery):
    category = callback_query.data.split('category ')[-1]
    await bot.answer_callback_query(callback_query.id)
    start_buttons = [f'Случайный ({category})' if category != RANDOM_CATEGORY_LABEL else 'Случайный', 'Изменить Категорию']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    # await send_joke(
    #     chat_id=callback_query.from_user.id,
    #     joke=await get_joke_from_category(category),
    #     category=category,
    #     top_text="По Категории",
    # )
    await change_default_category(callback_query.from_user.id, category)
    await bot.send_message(callback_query.from_user.id, f'Категория Изменена на "{category}"', reply_markup=keyboard)


def main():
    executor.start_polling(dp, skip_updates=True)


if __name__ == '__main__':
    main()
