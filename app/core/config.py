import logging
from logging.handlers import RotatingFileHandler

from pydantic import BaseSettings

from app.core.constants import log_constants


class Settings(BaseSettings):
    app_title: str = 'QRKot'
    description: str = (
        'Приложение для Благотворительного '
        'фонда поддержки котиков QRKot'
    )
    database_url: str = 'sqlite+aiosqlite:///./charity_fund.db'
    secret: str = 'SECRET'

    class Config:
        env_file = '.env'


def configure_logging():
    log_dir = log_constants.BASE_DIR / 'logs'
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / 'charity_fund.log'
    rotating_handler = RotatingFileHandler(
        log_file,
        maxBytes=log_constants.MAX_BYTES,
        backupCount=log_constants.BACKUP_COUNT
    )
    logging.basicConfig(
        datefmt=log_constants.DT_FORMAT,
        format=log_constants.LOG_FORMAT,
        level=logging.INFO,
        handlers=(rotating_handler, logging.StreamHandler())
    )


settings = Settings()
