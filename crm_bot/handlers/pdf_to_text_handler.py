import os.path

from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery, ContentTypes
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from config import logger
from decorators.for_handlers import check_message_private
from classes.keyboards_classes import StartMenu
from classes.url_finder import URLFinder
from states import UserState


@check_message_private
@logger.catch
async def ask_file_to_recognize(message: Message):
    await message.answer("Отправьте файл для распознавания.", reply_markup=StartMenu.cancel_keyboard())
    await UserState.wait_pdf_file.set()


@logger.catch
async def wait_file(message: Message, state: FSMContext):
    doc = message.document
    directory: str = 'files'
    file_name: str = doc.file_name
    path: str = os.path.join(directory, file_name)
    await doc.download(destination_file=path)
    logger.debug(f'File saved {path}')
    result = URLFinder(path).get_links()
    text = '\n'.join(result)
    await message.answer(
        f'Ссылки из файла {file_name}:'
        f'\n{text}',
        disable_web_page_preview=True,
        disable_notification=True
    )
    await state.finish()


def register_pdf_handlers(dp: Dispatcher) -> None:
    dp.register_message_handler(ask_file_to_recognize, Text(equals=[StartMenu.pdf_to_text]))
    dp.register_message_handler(wait_file, content_types=ContentTypes.DOCUMENT, state=UserState.wait_pdf_file)
