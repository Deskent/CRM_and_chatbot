import aiogram.utils.exceptions
from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery
from datastructurepack import DataStructure

from classes.api_requests import UserAPI
from classes.errors_reporter import MessageReporter
from classes.keyboards_classes import get_categories_keyboard, StartMenu, YesNo, button_contact
from classes.worksheets import Category, Worksheet
from config import logger, bot, settings
from decorators.for_handlers import check_message_private
from states import UserState


@check_message_private
@logger.catch
async def ask_name_handler(message: Message, state: FSMContext):
    userdata = Worksheet()
    userdata.username = '@' + message.from_user.username if message.from_user.username else '-'
    userdata.first_name = message.from_user.first_name if message.from_user.first_name else '-'
    userdata.last_name = message.from_user.last_name if message.from_user.last_name else '-'
    userdata.telegram_id = message.from_user.id
    await state.update_data(userdata=userdata)
    if userdata.username == '-':
        text = (
            "У вас не указано имя пользователя телеграм, "
            "наши специалисты не смогут связаться с вами.\n"
            "Хотите оставить другой способ связи или поделиться телефоном?"
        )
        keyboard = YesNo.keyboard(
            yes_key='Другой способ',
            prefix='another_contact',
            splitter='',
            no_key='Поделиться телефоном',
            negative_callback='share_phone'
        )
        await message.answer(text, reply_markup=keyboard)
        await UserState.enter_another_contact.set()
        return
    text = 'Введите имя:'
    await message.answer(text, reply_markup=StartMenu.cancel_keyboard())
    await UserState.enter_name.set()


async def enter_another_contact(callback: CallbackQuery):
    await callback.message.delete()

    if callback.data == 'another_contact':
        await callback.message.answer(
            'Введите контактные данные', reply_markup=StartMenu.cancel_keyboard())
        await UserState.enter_contact_data.set()
        return
    elif callback.data == 'share_phone':
        await callback.message.answer(
            "Я соглашаюсь поделиться телефоном.", reply_markup=button_contact()
        )
        await UserState.share_phone.set()
        return


async def add_phone_number(message: Message, state: FSMContext):
    phone = message.contact.phone_number
    data: dict = await state.get_data()
    userdata: Worksheet = data['userdata']
    userdata.username = phone
    await state.update_data(userdata=userdata)
    text = 'Введите имя:'
    await message.answer(text, reply_markup=StartMenu.cancel_keyboard())
    await UserState.enter_name.set()


async def add_another_contact(message: Message, state: FSMContext):
    data: dict = await state.get_data()
    userdata: Worksheet = data['userdata']
    userdata.username = message.text
    await state.update_data(userdata=userdata)
    text = 'Введите имя:'
    await message.answer(text, reply_markup=StartMenu.cancel_keyboard())
    await UserState.enter_name.set()


async def choose_interview(message: Message, state: FSMContext):
    await state.set_state(UserState.interview)

    data: dict = await state.get_data()
    userdata: Worksheet = data['userdata']
    userdata.name = message.text
    await state.update_data(userdata=userdata)

    text = 'Выберите категорию:'
    categories: dict[int, str] = await UserAPI.get_categories()
    if not categories:
        await MessageReporter.send_report_to_admins('Categories not found.')
    Category.categories = categories
    await message.answer(text, reply_markup=get_categories_keyboard(categories))


async def start_interview(callback: CallbackQuery, state: FSMContext):
    category_id: int = int(callback.data.split('_')[-1])
    data: dict = await state.get_data()
    userdata: Worksheet = data['userdata']
    userdata.category_id = category_id
    poll: list[str] = await UserAPI.get_poll_by_category(category_id)
    if not poll:
        await state.finish()
        await finish_interview(callback.message, userdata=userdata)
        return
    userdata.poll = [[question] for question in poll]
    current_index = 0
    current_question: str = userdata.poll[current_index][0]

    await state.update_data(userdata=userdata, current_index=current_index)

    await callback.answer(f'start poll {callback.data}')
    await callback.message.answer(current_question)


async def ask_question(message: Message, state: FSMContext):
    data = await state.get_data()
    userdata: Worksheet = data['userdata']
    current_index = data.get('current_index')
    userdata.poll[current_index].append(message.text)
    current_index += 1
    if current_index >= len(userdata.poll):
        await state.finish()
        await finish_interview(message, userdata=userdata)
        return

    current_question: str = userdata.poll[current_index][0]

    await state.update_data(userdata=userdata, current_index=current_index)
    await message.answer(current_question)


async def finish_interview(message: Message, userdata: Worksheet):

    text = "Ваша заявка:"
    await message.answer(text, reply_markup=StartMenu.keyboard())
    answers: str = '\n'.join(f"{elem[0]}\n{elem[1]}" for elem in userdata.poll)
    order_text = (
        f"\nИмя: {userdata.name}"
        f"\nКатегория: {Category.categories[str(userdata.category_id)]}"
        f"\nВопросы:\n{answers}"
    )

    logger.debug(f'Userdata: {userdata.as_dict()}')

    await message.answer(order_text, reply_markup=StartMenu.keyboard())

    result: 'DataStructure' = await UserAPI.send_worksheet(userdata=userdata.as_dict())
    text = 'Заявка не отправлена.'
    if result and result.status in range(200, 300):
        text = 'Заявка отправлена.'
        try:
            new_order_text = (
                f"Новая заявка:"
                f"\n{order_text}"
                f"\nКлиент: {userdata.username}"
            )
            await bot.send_message(
                chat_id=f'-100{settings.GROUP_ID}',
                text=new_order_text
            )
        except aiogram.utils.exceptions.NeedAdministratorRightsInTheChannel as err:
            logger.exception(err)
            await MessageReporter.send_report_to_admins('Бот должен быть администратором')
        except Exception as err:
            logger.exception(err)
    await message.answer(text, reply_markup=StartMenu.keyboard())


def register_polls_handlers(dp: Dispatcher) -> None:
    dp.register_message_handler(ask_name_handler, Text(equals=[StartMenu.worksheet]))
    dp.register_message_handler(choose_interview, state=UserState.enter_name)
    dp.register_callback_query_handler(
        enter_another_contact, state=[UserState.enter_another_contact])
    dp.register_message_handler(
        add_phone_number, content_types=['contact'], state=UserState.share_phone)
    dp.register_message_handler(add_another_contact, state=UserState.enter_contact_data)
    dp.register_callback_query_handler(start_interview, state=[UserState.interview])
    dp.register_message_handler(ask_question, state=[UserState.interview])
