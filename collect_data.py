from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from contextlib import contextmanager
import time
import sqlite3
import aiosqlite
import asyncio
import aiohttp

import config


@contextmanager
def timed(message: str = 'timed: ', precision: int = 3) -> None:
    before = time.time()
    yield
    after = time.time()
    took = round(after - before, precision)
    print(message.format(took) if '{}' in message else f'{message}{took}')


def create_db_table(db_data: dict[str]) -> None:
    with sqlite3.connect(db_data['name']) as db:
        db.execute(f'''
            CREATE TABLE IF NOT EXISTS {db_data['table']} (
                id       INTEGER PRIMARY KEY,
                joke     TEXT,
                category TEXT
            );
            CREATE TABLE IF NOT EXISTS users (
                id               INTEGER PRIMARY KEY,
                user_id          INTEGER,
                default_category TEXT
            );
        ''')
        db.commit()


async def save_to_db(db_data: dict[str: str], jokes: list[str, str], category: str) -> None:
    async with aiosqlite.connect(db_data['name']) as db:
        for joke in jokes:
            await db.execute(f'''
                INSERT INTO {db_data['table']}
                (joke, category)
                VALUES(?, ?)
            ''', (joke, category))
        await db.commit()


def get_categories(src: str) -> list[tuple[str, str]]:
    soup = BeautifulSoup(src, 'lxml')
    category_items = soup.find_all('a', class_='menuanekdot')
    # removing unwanted categories
    category_items = category_items[7:-2]
    for i in 13, 7, 6, 4:
        del category_items[i]
    # return [(f'https://anekdotov.net{c.get("href")}', c.text.strip()) for c in category_items]
    category_data = [(f'https://anekdotov.net{c.get("href")}', c.text.strip().capitalize()) for c in category_items]
    return category_data


async def get_page_data(session: aiohttp.ClientSession, url: str) -> str:
    response = await session.get(url=url)
    return await response.text()


async def parse_jokes(src: str) -> list[str, str]:
    soup = BeautifulSoup(src, 'lxml')
    jokes_items = soup.find_all('div', class_='anekdot')
    jokes = [j.text.strip() for j in jokes_items]
    return jokes


async def gather_data(db_data: dict[str]) -> None:
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'user-agent': UserAgent().random,
    }
    url = 'https://anekdotov.net'
    tasks = []

    async with aiohttp.ClientSession() as session:
        response = await session.get(url=url, headers=headers)

        for link, category_name in get_categories(await response.text()):
            for page in range(0, 36):
                tasks.append(asyncio.create_task(save_to_db(db_data, await parse_jokes(
                    await get_page_data(session, f'{link}index-page-{page}.html')), category_name)))

        await asyncio.gather(*tasks)


def main():
    db_data = config.db_data
    create_db_table(db_data)
    asyncio.run(gather_data(db_data))


if __name__ == '__main__':
    with timed('Scrapping took {} seconds.'):
        main()
