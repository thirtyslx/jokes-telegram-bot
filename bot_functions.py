import aiosqlite

from config import DB_NAME, DB_TABLE_JOKES, DB_TABLE_USERS, RANDOM_CATEGORY_LABEL


async def get_random_joke(
        db_name: str = DB_NAME,
        db_table_jokes: str = DB_TABLE_JOKES,
) -> tuple[str, str]:
    async with aiosqlite.connect(db_name) as db:
        cursor = await db.execute(f'SELECT joke, category FROM {db_table_jokes} ORDER BY RANDOM() LIMIT 1')
        joke, category = await cursor.fetchone()
        return joke, category


async def get_joke_from_category(
        category: str,
        db_name: str = DB_NAME,
        db_table_jokes: str = DB_TABLE_JOKES,
) -> str:
    async with aiosqlite.connect(db_name) as db:
        query = f'SELECT joke FROM {db_table_jokes} WHERE category = "{category}" ORDER BY RANDOM() LIMIT 1'
        cursor = await db.execute(query)
        joke = await cursor.fetchone()
        return joke[0]


async def get_categories(
        db_name: str = DB_NAME,
        db_table_jokes: str = DB_TABLE_JOKES,
) -> list[str, str]:
    async with aiosqlite.connect(db_name) as db:
        cursor = await db.execute(f'SELECT DISTINCT category FROM {db_table_jokes}')
        categories = [el[0] for el in await cursor.fetchall()]
        categories.insert(0, RANDOM_CATEGORY_LABEL)
        return categories


async def change_default_category(
        user_id: int,
        category: str,
        is_new_user: bool = False,
        db_name: str = DB_NAME,
):
    async with aiosqlite.connect(db_name) as db:
        if is_new_user:
            await db.execute(f'''
                DELETE FROM users
                WHERE user_id = "{user_id}"
            ''')
            await db.execute(f'''
                INSERT INTO users
                (user_id, default_category)
                VALUES("{user_id}", "{category}")
            ''')
        else:
            await db.execute(f'''
            UPDATE users
            SET user_id = "{user_id}", default_category = "{category}"
            WHERE user_id = {user_id}
        ''')
        await db.commit()


async def get_default_category(
        user_id: int,
        db_name: str = DB_NAME,
        db_table_users: str = DB_TABLE_USERS,
):
    async with aiosqlite.connect(db_name) as db:
        cursor = await db.execute(f'SELECT default_category FROM {db_table_users} WHERE user_id = "{user_id}"')
        category = await cursor.fetchone()
        return category[0]
