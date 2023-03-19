from loguru import logger
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import bot.database
# from bot.filters import register_all_filters
from bot.misc import Config
from bot.handlers import register_all_handlers
from bot.database.models import register_models


async def __on_start_up(dp: Dispatcher) -> None:
    logger.info('Bot starts')
    register_models()
    register_all_handlers(dp)


def __start_telegram_bot() -> None:
    bot = Bot(token=Config.TOKEN, parse_mode='HTML')
    dp = Dispatcher(bot, storage=MemoryStorage())
    executor.start_polling(dp, skip_updates=True, on_startup=__on_start_up)


def __main() -> None:
    if not Config.DEBUG:
        log_path = 'bot.log'
        logger.add(log_path, format='{time} {level} {message}', rotation='10:00', compression='zip', retention='3 days')
    __start_telegram_bot()


if __name__ == '__main__':
    __main()
