from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def make_button(text: str, callback_data: str) -> InlineKeyboardButton:
    return InlineKeyboardButton(text=text, callback_data=callback_data)


def make_keyboard(buttons: list[dict]) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    for button in buttons:
        keyboard.add(make_button(**button))
    return keyboard
