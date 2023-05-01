from aiogram.dispatcher.filters.state import State, StatesGroup


class OpenLessonRegisterState(StatesGroup):
    table_name = State()
    full_name = State()
    tel = State()
    chat_id = State()
    user_name = State()
