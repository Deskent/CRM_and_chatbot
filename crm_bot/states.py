from aiogram.dispatcher.filters.state import State, StatesGroup

class MyState(StatesGroup):
    first_state = State()
    second_state = State()