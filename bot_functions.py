import aiosqlite

import config


async def get_random_joke(
        db_name: str = config.db_data['name'],
        table: str = config.db_data['table'],
) -> tuple[str, str]:
    async with aiosqlite.connect(db_name) as db:
        cursor = await db.execute(f'SELECT joke, category FROM {table} ORDER BY RANDOM() LIMIT 1')
        joke, category = await cursor.fetchone()
        return joke, category


async def get_joke_from_category(
        category: str,
        db_name: str = config.db_data['name'],
        table: str = config.db_data['table'],
) -> str:
    async with aiosqlite.connect(db_name) as db:
        query = f'SELECT joke FROM {table} WHERE category = "{category}" ORDER BY RANDOM() LIMIT 1'
        cursor = await db.execute(query)
        joke = await cursor.fetchone()
        return joke[0]


async def get_categories(
        db_name: str = config.db_data['name'],
        table: str = config.db_data['table'],
) -> list[str, str]:
    async with aiosqlite.connect(db_name) as db:
        cursor = await db.execute(f'SELECT DISTINCT category FROM {table}')
        categories = [el[0] for el in await cursor.fetchall()]
        categories.insert(0, config.random_category_label)
        return categories


async def change_default_category(user_id: int, category: str, update: bool = True):
    async with aiosqlite.connect(config.db_data['name']) as db:
        if update:
            await db.execute(f'''
                UPDATE users
                SET user_id = "{user_id}", default_category = "{category}"
                WHERE user_id = {user_id}
            ''')
        else:
            await db.execute(f'''
                DELETE FROM users
                WHERE user_id = "{user_id}"
            ''')
            await db.execute(f'''
                INSERT INTO users
                (user_id, default_category)
                VALUES("{user_id}", "{category}")
            ''')
        await db.commit()


async def get_default_category(user_id: int):
    async with aiosqlite.connect(config.db_data['name']) as db:
        cursor = await db.execute(f'SELECT default_category FROM users WHERE user_id = "{user_id}"')
        category = await cursor.fetchone()
        return category[0]
