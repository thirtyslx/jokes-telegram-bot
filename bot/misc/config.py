from os import environ
from typing import Final


class Config:
    TOKEN: Final = environ.get('TOKEN', 'define me')
    DEBUG: Final = bool(len(environ.get('DEBUG', '')))
    BLACKLIST = [13, 7, 6, 4]

    # Label, that means 'random category'
    RAND_CATEGORY: Final = 'СЛУЧАЙНАЯ'
    RAND_BTN: Final = 'Случайный анекдот'

    JOKES_COPYRIGHT: Final = 'www.anekdotov.net'
