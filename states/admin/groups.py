from aiogram.dispatcher.filters.state import State, StatesGroup


class GroupAddState(StatesGroup):
    group_id = State()
    group_name = State()
    lesson_days = State()
    lesson_time = State()
    confirmation = State()
