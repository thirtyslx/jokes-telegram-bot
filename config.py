from os import environ

DB_NAME = 'jokes.db'
DB_TABLE_JOKES = 'jokes'
DB_TABLE_USERS = 'users'

BOT_TOKEN = environ.get('TOKEN', 'define me!')

# Label, that means 'random category'
RANDOM_CATEGORY_LABEL = 'СЛУЧАЙНАЯ'
