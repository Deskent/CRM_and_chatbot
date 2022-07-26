from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext

from config import logger, Dispatcher, bot
from classes.keyboards_classes import BaseMenu, StartMenu
from decorators.for_handlers import check_message_private


@logger.catch
async def callback_cancel_handler(callback: CallbackQuery, state: FSMContext) -> None:
    """Ловит коллбэк инлайн кнопки Отмена и вызывает обработик для нее"""

    await send_cancel_message(
        telegram_id=callback.from_user.id, name=callback.from_user.username, state=state
    )
    await callback.answer()


@logger.catch
async def message_cancel_handler(message: Message, state: FSMContext) -> None:
    """Ловит сообщение или команду отмена, Отмена, cancel и вызывает обработик для нее"""

    await send_cancel_message(
        telegram_id=message.from_user.id, name=message.from_user.username, state=state)


@logger.catch
async def send_cancel_message(telegram_id: int, name: str, state: FSMContext) -> None:
    """
    Отменяет текущие запросы и сбрасывает состояние.
    Ставит пользователя в нерабочее состояние.
    Обработчик команды /cancel, /Отмена, кнопки Отмена и инлайн кнопки Отмена
    """
    await bot.send_message(
        chat_id=telegram_id,
        text="Вы отменили текущую команду",
        reply_markup=StartMenu.keyboard()
    )
    logger.debug(f"\n\tUser: {name}:{telegram_id}: canceled command.")
    await state.finish()


@logger.catch
def register_cancel_handlers(dp: Dispatcher) -> None:
    """
    Регистратор для функций данного модуля
    """

    dp.register_message_handler(message_cancel_handler, commands=[BaseMenu.cancel_key], state="*")
    dp.register_message_handler(
        message_cancel_handler, Text(startswith=[BaseMenu.cancel_key], ignore_case=True), state="*")
    dp.register_callback_query_handler(
        callback_cancel_handler, Text(startswith=[BaseMenu.cancel_key], ignore_case=True), state="*")
