from aiogram.dispatcher.filters.state import State, StatesGroup


class UserState(StatesGroup):
    enter_name = State()
    enter_link = State()
    enter_category = State()
    enter_price = State()
    was_advertised = State()
    what_after = State()
