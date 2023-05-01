from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton


def generate_cancel_btn():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(
        KeyboardButton(text="❌ Отменить действия")
    )
    return markup
