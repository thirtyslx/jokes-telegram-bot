from os import environ
from typing import Final


class Config:
    TOKEN: Final = environ.get('TOKEN', 'define me')
    DEBUG: Final = bool(len(environ.get('DEBUG', '')))
    BLACKLIST_CATEGORY_IDS = tuple(map(int, environ.get('BLACKLIST_CATEGORY_IDS', ()).split(', ')))
    ADMINS = tuple(map(int, environ.get('ADMINS', ()).split(', ')))

    RAND_CATEGORY: Final = 'СЛУЧАЙНАЯ'
    RAND_BTN: Final = 'Случайный анекдот'

    JOKES_COPYRIGHT: Final = 'www.anekdotov.net'
