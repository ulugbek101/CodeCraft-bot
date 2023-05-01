from aiogram.dispatcher.filters.state import State, StatesGroup


class CoursesState(StatesGroup):
    name = State()
    desc = State()
    image_path = State()

