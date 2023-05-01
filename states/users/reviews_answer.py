from aiogram.dispatcher.filters.state import State, StatesGroup


class ReviewsAnswerState(StatesGroup):
    user_id = State()
    body = State()
