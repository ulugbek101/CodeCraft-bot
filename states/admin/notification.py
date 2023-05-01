from aiogram.dispatcher.filters.state import StatesGroup, State


class NotificationState(StatesGroup):
    body = State()
