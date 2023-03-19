from os import environ
from typing import Final


class Config:
    TOKEN: Final = environ.get('TOKEN', 'define me')
    DEBUG: Final = bool(len(environ.get('DEBUG', '')))

    DB_NAME: Final = 'jokes.db'
    DB_TABLE_JOKES: Final = 'jokes'
    DB_TABLE_USERS: Final = 'users'

    # Label, that means 'random category'
    RAND_CATEGORY: Final = 'СЛУЧАЙНАЯ'
    RAND_BTN: Final = 'Случайный анекдот'
