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

    @classmethod
    @logger.catch
    def keyboard(cls) -> 'ReplyKeyboardMarkup':
        """Возвращает кнопочки меню для канала из списка"""

        return default_keyboard().add(
            KeyboardButton(cls.worksheet),
            KeyboardButton(cls.help),
            KeyboardButton(cls.cancel_key),
        )


@dataclass
class YesNo:

    @classmethod
    @logger.catch
    def keyboard(
            cls,
            prefix: str,
            suffix: str,
            cancel_callback: str = BaseMenu.cancel_key,
            yes_key: str = 'Да',
            no_key: str = BaseMenu.cancel_key,
            splitter: str = '_'
    ) -> 'InlineKeyboardMarkup':
        """Возвращает кнопочку Отмена"""

        return InlineKeyboardMarkup(row_width=2
        ).add(
            InlineKeyboardButton(text=yes_key, callback_data=f'{prefix}{splitter}{suffix}')
        ).add(
            InlineKeyboardButton(text=no_key, callback_data=cancel_callback)
        )


def get_categories() -> InlineKeyboardMarkup:
    categories = {
        'target': 'Таргетированная реклама',
        'content': 'Контент',
        'strategy': 'Составление стратегии',
        'consult': 'Консультация',
    }
    keyboard = InlineKeyboardMarkup(row_width=1)
    for key, name in categories.items():
        keyboard.add(InlineKeyboardButton(
            text=name,
            callback_data=f'category_{key}'
        ))
    return keyboard

#
# @dataclass(frozen=True)
# class ProductsMenu(BaseMenu):
#     """Список всех товаров"""
#
#     @classmethod
#     @logger.catch
#     async def keyboard(cls, callback_prefix: str) -> 'InlineKeyboardMarkup':
#         keyboard = InlineKeyboardMarkup(row_width=1)
#         for elem in await ProductAPI.get_all_products():
#             keyboard.add(InlineKeyboardButton(
#                 text=elem.get('name'),
#                 callback_data=f'{callback_prefix}_{elem.get("id")}'
#             ))
#
#         return keyboard
#
#
# @dataclass(frozen=True)
# class AdminMenu(BaseMenu):
#     """Админское меню"""
#
#     admin: str = 'admin'
#     add_product: str = 'Добавить товар'
#     delete_product: str = 'Удалить товар'
#     set_user_admin: str = 'Назначить админа'
#     set_channel: str = 'Добавить канал'
#
#     @classmethod
#     @logger.catch
#     def keyboard(cls) -> 'ReplyKeyboardMarkup':
#         """Возвращает кнопочки меню для канала из списка"""
#
#         return default_keyboard().add(
#             KeyboardButton(cls.add_product),
#             KeyboardButton(cls.delete_product),
#             KeyboardButton(cls.set_user_admin),
#             KeyboardButton(cls.set_channel),
#             KeyboardButton(cls.cancel_key),
#         )
#
#     @classmethod
#     @logger.catch
#     def get_prefix(cls, prefix: str) -> str:
#         """Возвращает префикс для отлова коллбэка по имени команды"""
#
#         return {
#             cls.add_product: 'addproduct',
#             cls.delete_product: 'deleteproduct',
#         }[prefix]
#
#
# @dataclass
# class YesNo:
#
#     @classmethod
#     @logger.catch
#     def keyboard(
#             cls,
#             prefix: str,
#             suffix: str,
#             cancel_callback: str = BaseMenu.cancel_key,
#             yes_key: str = 'Да',
#             no_key: str = BaseMenu.cancel_key,
#             splitter: str = '_'
#     ) -> 'InlineKeyboardMarkup':
#         """Возвращает кнопочку Отмена"""
#
#         return InlineKeyboardMarkup(row_width=2
#         ).add(
#             InlineKeyboardButton(text=yes_key, callback_data=f'{prefix}{splitter}{suffix}')
#         ).add(
#             InlineKeyboardButton(text=no_key, callback_data=cancel_callback)
#         )
#
#
# @dataclass(frozen=True)
# class InformationMenu(BaseMenu):
#     """Меню информации"""
#
#     balance: str = 'Баланс'
#     licenses: str = 'Лицензии'
#
#     @classmethod
#     @logger.catch
#     def keyboard(cls) -> 'ReplyKeyboardMarkup':
#         """Возвращает кнопочки из списка"""
#
#         return default_keyboard().add(
#             KeyboardButton(cls.balance),
#             KeyboardButton(cls.licenses),
#             KeyboardButton(cls.cancel_key),
#         )
