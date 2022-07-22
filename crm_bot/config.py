from aiogram import Bot, Dispatcher
from pydantic import BaseSettings
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from myloguru.my_loguru import get_logger


class Settings(BaseSettings):
    STAGE: str = 'undefined'
    LOGGING_LEVEL: int = 20
    TELEBOT_TOKEN: str = ''
    ADMINS: list = []
    DEBUG: bool = False
    BASE_API_URL: str


settings = Settings(_env_file='.env', _env_file_encoding='utf-8')

# DEBUG settings
logger = get_logger(settings.LOGGING_LEVEL)

# configure bot
tgToken: str = settings.TELEBOT_TOKEN
bot = Bot(token=tgToken)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
