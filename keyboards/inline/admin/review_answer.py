from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def generate_review_answer_keyboard(text: str, user_id: int, state: int):
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton(text=f"{text}", callback_data=f"review-answer:{state}-{user_id}")
    )
    return markup
