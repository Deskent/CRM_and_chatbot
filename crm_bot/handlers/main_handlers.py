"""Модуль с основными обработчиками команд, сообщений и коллбэков"""

from aiogram.types import Message

from classes.keyboards_classes import StartMenu
from config import logger, Dispatcher
from _resources import __version__
from decorators.for_handlers import check_message_private


@check_message_private
@logger.catch
async def my_id(message: Message):
    await message.answer(message.from_user.id)


@check_message_private
@logger.catch
async def default_handler(message: Message) -> None:
    """Ответ на любое необработанное действие активного пользователя."""

    await message.answer(
        f'Welcome to bot.\nCurrent version: {__version__}',
        reply_markup=StartMenu.keyboard())


@logger.catch
def register_main_handlers(dp: Dispatcher) -> None:
    """
    Регистратор для функций данного модуля
    """

    dp.register_message_handler(my_id, commands=['myid'])
    dp.register_message_handler(default_handler)
