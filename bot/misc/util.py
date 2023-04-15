from loguru import logger
import shutil

from bot.misc import PathControl


def backup_database() -> None:
    shutil.copy(PathControl.get('bot/database/jokes.db'), PathControl.get('bot/database/jokes.db.bak'))
    logger.info('Backed up database')


def restore_database_from_backup() -> None:
    shutil.copy(PathControl.get('bot/database/jokes.db.bak'), PathControl.get('bot/database/jokes.db'))
    logger.info('Restored database backup')
