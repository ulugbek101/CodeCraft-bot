from aiogram.dispatcher.filters.state import State, StatesGroup


class CourseRegisterState(StatesGroup):
    course = State()
    fullname = State()
    tel = State()
    username = State()
