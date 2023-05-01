from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def generate_send_contact_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(
        KeyboardButton(text="📞 Поделиться номером", request_contact=True)
    )
    markup.row(
        KeyboardButton(text="❌ Отменить действия")
    )
    return markup
