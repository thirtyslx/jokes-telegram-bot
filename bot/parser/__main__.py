from typing import Tuple
from loguru import logger

from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from contextlib import contextmanager
import time
import sqlite3
import aiosqlite
import asyncio
from asyncio import create_task
from aiohttp import ClientSession
from itertools import product

import bot.database
from bot.database.methods.insert import save_joke
from bot.database.methods.delete import delete_all_jokes
import config


# session = None
# data: tuple[list[str, str]] = tuple()


@contextmanager
def timed(message: str = 'timed: ', precision: int = 3) -> None:
    before = time.time()
    yield
    after = time.time()
    took = round(after - before, precision)
    logger.info(message.format(took) if '{}' in message else f'{message}{took}')


async def save_to_db(*args):
    print(args[1:])


async def get_categories(s: ClientSession):  # -> list[tuple[str, str]]:
    soup = await get_page_soup(s, 'https://anekdotov.net')
    category_items = soup.find_all('a', class_='menuanekdot')
    # removing unwanted categories
    category_items = category_items[7:-2]
    category_items = category_items[0:1]
    # for i in 13, 7, 6, 4:
    #     del category_items[i]
    # return [(f'https://anekdotov.net{c.get("href")}', c.text.strip()) for c in category_items]
    category_data = [(f'https://anekdotov.net{c.get("href")}', c.text.strip().capitalize()) for c in category_items]
    return category_data


async def get_page_soup(s: ClientSession, url: str) -> BeautifulSoup:
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'user-agent': UserAgent().random,
    }
    response = await s.get(url=url, headers=headers)
    soup = BeautifulSoup(await response.text(), 'lxml')
    return soup


async def get_jokes_from_page(s: ClientSession, url: str) -> list[str, str]:
    soup = await get_page_soup(s, url)
    jokes = [j.text.strip() for j in soup.find_all('div', class_='anekdot')]
    return jokes


async def log(category: str, page: int):
    logger.info(f'Collecting: {category} - {page + 1}/36')


async def gather_data(db_data: dict[str] = None) -> None:
    delete_all_jokes()
    logger.info('Deleted all jokes from db')
    # await save_joke('JOkkea', 'category36')
    # return
    # noinspection PyUnreachableCode
    with timed('Gathered data in {} seconds'):
        logger.info('Started gathering data')
        async with ClientSession() as s:
            tasks = []
            for link, category in await get_categories(s):
                for page in range(0, 36):
                    create_task(log(category, page))
                    tasks.append(
                        create_task(save_joke(jokes=await get_jokes_from_page(s, f'{link}index-page-{page}.html'),
                                              category=category)))
    # await asyncio.gather(*tasks)
    # noinspection PyUnreachableCode
    # for link, category_name in get_categories():
    #     for page in range(0, 36):
    #         tasks.append(asyncio.create_task(save_to_db(db_data, await get_jokes_from_page(
    #             await get_page_soup(session, f'{link}index-page-{page}.html')), category_name)))
    # await asyncio.gather(*tasks)
    #


def main():
    # db_data = config.db_data
    # create_db_table(db_data)

    # from bot.database import register_models
    # register_models()
    # delete_all_jokes()
    asyncio.run(gather_data())


if __name__ == '__main__':
    with timed('Scrapping took {} seconds.'):
        main()
