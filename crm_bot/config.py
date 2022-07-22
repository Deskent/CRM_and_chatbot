from aiogram import Bot, Dispatcher
from pydantic import BaseSettings
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from myloguru.my_loguru import get_logger

from classes.bot_texts import BotTexts


class Settings(BaseSettings):
    TELEBOT_TOKEN: str
    ADMINS: list
    LOGGING_LEVEL: int = 20
    DEBUG: bool = False
    STAGE: str = 'undefined'
    BASE_API_URL: str
    DB_KEY_VALIDATION: str


settings = Settings(_env_file='.env', _env_file_encoding='utf-8')

# DEBUG settings
logger = get_logger(settings.LOGGING_LEVEL)

# configure bot
tgToken: str = settings.TELEBOT_TOKEN
bot = Bot(token=tgToken)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

bot_texts = BotTexts()
