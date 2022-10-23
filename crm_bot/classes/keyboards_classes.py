from dataclasses import dataclass
from typing import Union

from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton,
    ReplyKeyboardRemove
)

from config import logger


def default_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True,
        row_width=3
    )


@dataclass(frozen=True)
class BaseMenu:
    cancel_key: str = 'Отмена'

    @classmethod
    @logger.catch
    def keyboard(cls) -> Union[ReplyKeyboardMarkup, InlineKeyboardMarkup]:
        """Возвращает кнопочку Отмена"""

        return default_keyboard().add(KeyboardButton(cls.cancel_key))

    @classmethod
    @logger.catch
    def cancel_keyboard(cls) -> Union[ReplyKeyboardMarkup, InlineKeyboardMarkup]:
        """Возвращает кнопочку Отмена"""

        return BaseMenu.keyboard()


@dataclass(frozen=True)
class StartMenu(BaseMenu):
    """Стандартное пользовательское меню"""

    worksheet: str = 'Пройти опрос'
    help: str = 'Помощь'
    pdf_to_text: str = 'Распознать PDF ссылки'

    @classmethod
    @logger.catch
    def keyboard(cls) -> 'ReplyKeyboardMarkup':
        """Возвращает кнопочки меню для канала из списка"""

        return default_keyboard().add(
            KeyboardButton(cls.worksheet),
            KeyboardButton(cls.help),
            KeyboardButton(cls.pdf_to_text),
            KeyboardButton(cls.cancel_key),
        )


@dataclass
class YesNo:

    @classmethod
    @logger.catch
    def keyboard(
            cls,
            yes_key: str = 'Да',
            no_key: str = BaseMenu.cancel_key,
            prefix: str = '',
            splitter: str = '_',
            suffix: str = '',
            negative_callback: str = BaseMenu.cancel_key
    ) -> 'InlineKeyboardMarkup':
        """Возвращает две кнопки с настраиваемым колбэками и текстами"""

        return InlineKeyboardMarkup(row_width=2
        ).add(
            InlineKeyboardButton(text=yes_key, callback_data=f'{prefix}{splitter}{suffix}')
        ).add(
            InlineKeyboardButton(text=no_key, callback_data=negative_callback)
        )


def get_categories_keyboard(categories: dict[int, str]) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)
    for id, name in categories.items():
        keyboard.add(InlineKeyboardButton(
            text=name,
            callback_data=f'category_{id}'
        ))
    return keyboard


@logger.catch
def button_contact() -> ReplyKeyboardMarkup:
    """Возвращает кнопку 'Отправить контакт'"""

    return default_keyboard().add(KeyboardButton(text='Отправить', request_contact=True))
