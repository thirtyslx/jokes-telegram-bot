from os import environ
db_data = {
    'name': 'jokes.db',
    'table': 'jokes',
}
token = environ.get('TOKEN', 'define me!')
random_category_label = 'СЛУЧАЙНАЯ'
