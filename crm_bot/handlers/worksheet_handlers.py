from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext
from datastructurepack import DataStructure

from classes.api_requests import UserAPI
from classes.keyboards_classes import StartMenu, get_categories, YesNo
from config import logger, Dispatcher, bot_texts
from classes.worksheets import Worksheet
from states import UserState


@logger.catch
async def ask_name_handler(message: Message, state: FSMContext):
    if not await UserAPI.update_texts():
        logger.warning('Texts update error.')
    userdata = Worksheet()
    userdata.username = message.from_user.username
    userdata.first_name = message.from_user.first_name
    userdata.last_name = message.from_user.last_name
    userdata.telegram_id = message.from_user.id
    await state.update_data(userdata=userdata)
    text = bot_texts.enter_name
    await message.answer(text, reply_markup=StartMenu.cancel_keyboard())
    await UserState.enter_name.set()


@logger.catch
async def ask_link_handler(message: Message, state: FSMContext):
    data: dict = await state.get_data()
    userdata: Worksheet = data['userdata']
    userdata.name = message.text
    await state.update_data(userdata=userdata)
    text = bot_texts.enter_link
    await message.answer(text, reply_markup=StartMenu.cancel_keyboard())
    await UserState.enter_link.set()


@logger.catch
async def ask_category_handler(message: Message, state: FSMContext):
    data: dict = await state.get_data()
    userdata: Worksheet = data['userdata']
    userdata.target_link = message.text
    await state.update_data(userdata=userdata)

    text = bot_texts.enter_category
    await message.answer(text, reply_markup=StartMenu.cancel_keyboard())
    text = bot_texts.category_list

    # TODO удалить заглушку:
    categories = {
        'target': 'Таргетированная реклама',
        'content': 'Контент',
        'strategy': 'Составление стратегии',
        'consult': 'Консультация',
    }

    # TODO раскомментировать когда АПИ будет выдавать категории и удалить заглушку выше
    # categories: dict = await UserAPI.get_categories()

    await message.answer(text, reply_markup=get_categories(categories))
    await UserState.enter_category.set()


@logger.catch
async def ask_price_handler(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    await callback.message.delete()

    category: str = callback.data.rsplit('_', maxsplit=1)[-1]
    data: dict = await state.get_data()
    userdata: Worksheet = data['userdata']
    userdata.category = category
    await state.update_data(userdata=userdata)

    text = bot_texts.enter_price
    await callback.message.answer(text, reply_markup=StartMenu.cancel_keyboard())
    await UserState.enter_price.set()


@logger.catch
async def ask_was_advertised_handler(message: Message, state: FSMContext):
    data: dict = await state.get_data()
    userdata: Worksheet = data['userdata']
    userdata.price = int(message.text)
    await state.update_data(userdata=userdata)

    text = bot_texts.was_advertised
    await message.answer(
        text,
        reply_markup=YesNo.keyboard(
            yes_key='Да',
            no_key='Нет',
            prefix='was_advertised',
            cancel_callback='not_advertised',
            splitter='',
            suffix=''
        )
    )
    await UserState.was_advertised.set()


@logger.catch
async def ask_what_after_handler(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    await callback.message.delete()

    data: dict = await state.get_data()
    userdata: Worksheet = data['userdata']
    userdata.was_advertised = 'was_advertised' == callback.data
    await state.update_data(userdata=userdata)

    text = bot_texts.what_after
    await callback.message.answer(text, reply_markup=StartMenu.cancel_keyboard())
    await UserState.what_after.set()


@logger.catch
async def complete_worksheet_handler(message: Message, state: FSMContext):
    data: dict = await state.get_data()
    userdata: Worksheet = data['userdata']
    userdata.what_after = message.text

    text = (
        f"Ваша заявка:"
        f"\nИмя: {userdata.name}"
        f"\nСсылка: {userdata.target_link}"
        f"\nКатегория: {userdata.category}"
        f"\nБюджет: {userdata.price}"
        f"\nРекламировали раньше? {'Да' if userdata.was_advertised else 'Нет'}"
        f"\nЧто дальше? {userdata.what_after}"
    )
    logger.debug(f'Userdata: {userdata.as_dict()}')
    await message.answer(text, reply_markup=StartMenu.keyboard())
    result: 'DataStructure' = await UserAPI.send_worksheet(userdata=userdata.as_dict())
    text = bot_texts.worksheet_not_ok
    if result and result.success:
        text = bot_texts.worksheet_ok
    await message.answer(text, reply_markup=StartMenu.keyboard())
    await state.finish()


@logger.catch
def register_worksheet_handlers(dp: Dispatcher) -> None:
    """
    Регистратор для функций данного модуля
    """

    dp.register_message_handler(ask_name_handler, Text(equals=[StartMenu.worksheet]))
    dp.register_message_handler(ask_link_handler, state=UserState.enter_name)
    dp.register_message_handler(ask_category_handler, state=UserState.enter_link)
    dp.register_callback_query_handler(ask_price_handler, state=UserState.enter_category)
    dp.register_message_handler(ask_was_advertised_handler, state=UserState.enter_price)
    dp.register_callback_query_handler(ask_what_after_handler, state=UserState.was_advertised)
    dp.register_message_handler(complete_worksheet_handler, state=UserState.what_after)
