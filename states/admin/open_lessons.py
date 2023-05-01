from aiogram.dispatcher.filters.state import State, StatesGroup


class OpenLessonState(StatesGroup):
    name = State()
    datetime = State()
