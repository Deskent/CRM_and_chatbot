import os
from typing import TypedDict

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv

load_dotenv()

NAME_PROJECT = os.getenv('NAME_PROJECT')

bot_token = os.getenv('TELEBOT_TOKEN')
bot = Bot(token=bot_token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

admins: list[int] = [int(os.getenv('VOVA_TELEGRAM_ID'))]

API_ID = 17018161
API_HASH = 'e19d25b25c62ab7ac4025b591c574b8a'

class MyButton(TypedDict):
    text: str
    callback_data: str
