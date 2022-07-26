from aiogram.dispatcher.filters.state import State, StatesGroup


class UserState(StatesGroup):
    enter_name = State()
    enter_another_contact = State()
    enter_contact_data = State()
    share_phone = State()
    interview = State()
