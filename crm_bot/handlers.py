from aiogram import Dispatcher
from aiogram.types import Message, InlineKeyboardMarkup
from loguru import logger

from config import MyButton, bot, admins
from keyboards import make_keyboard


@logger.catch
async def send_message_to_admin(text: str,
                                keyboard: InlineKeyboardMarkup = None) -> None:
    """Отправляет сообщение админам"""
    for admin_id in admins:
        try:
            await bot.send_message(
                chat_id=admin_id,
                text=text,
            )

        except Exception as err:
            logger.error(err)


async def my_id(message: Message):
    await message.answer(message.from_user.id)


async def start(message: Message):
    buttons: list[MyButton] = [
        MyButton(text='Ok', callback_data='ok_data'),
        MyButton(text='Forward', callback_data='Forward_data'),
        MyButton(text='Back', callback_data='back_data'),
    ]
    keyboard = make_keyboard(buttons=buttons)
    await message.answer(text='I am Grut', reply_markup=keyboard)


def register_handlers(dp: Dispatcher) -> None:
    dp.register_message_handler(my_id, commands=['myid'])
    dp.register_message_handler(start)
