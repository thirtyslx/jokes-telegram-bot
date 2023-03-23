from loguru import logger
from time import time
from contextlib import contextmanager

from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from aiohttp import ClientSession
import asyncio

from bot.database.methods.insert import save_joke
from bot.database.methods.delete import delete_all_jokes


@contextmanager
def __timed(message: str = 'timed: ', precision: int = 3) -> None:
    before = time()
    yield
    after = time()
    took = round(after - before, precision)
    logger.info(message.format(took) if '{}' in message else f'{message}{took}')


async def __get_categories(s: ClientSession) -> list[tuple[str, str]]:
    soup = await __get_page_soup(s, 'https://anekdotov.net')
    category_items = soup.find_all('a', class_='menuanekdot')
    # removing unwanted categories
    category_items = category_items[7:-2]
    # todo: remove slice
    category_items = category_items[0:1]
    # for i in 13, 7, 6, 4:
    #     del category_items[i]
    category_data = [(f'https://anekdotov.net{c.get("href")}', c.text.strip().capitalize()) for c in category_items]
    return category_data


async def __get_page_soup(s: ClientSession, url: str) -> BeautifulSoup:
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'user-agent': UserAgent().random,
    }
    response = await s.get(url=url, headers=headers)
    soup = BeautifulSoup(await response.text(), 'lxml')
    return soup


async def __get_jokes_from_page(s: ClientSession, url: str,
                                category: str, page: int) -> list[str, str]:
    logger.info(f'Collecting: {page + 1}/36 - {category}')
    soup = await __get_page_soup(s, url)
    jokes = [j.text.strip() for j in soup.find_all('div', class_='anekdot')]
    return jokes


async def gather_data() -> None:
    delete_all_jokes()
    with __timed('Gathered data in {} seconds'):
        logger.info('Started gathering data')
        async with ClientSession() as s:
            tasks = []
            for link, category in await __get_categories(s):
                for page in range(0, 36):
                    tasks.append(asyncio.create_task(
                        save_joke(jokes=await __get_jokes_from_page(s, f'{link}index-page-{page}.html', category, page),
                                  category=category)))
            await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(gather_data())
