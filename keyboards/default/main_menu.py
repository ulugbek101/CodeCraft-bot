from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from tools.menu_generating import generate_reply_keyboard_menu_buttons


def generate_main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(
        KeyboardButton(text="🔍 Узнать о курсах"),
        KeyboardButton(text="🖋📄 Записаться на пробный урок")
    )
    commands = (
        "⚙️ Настройки",
        "📌 Локация",
        "📞 Наши контакты",
        "📝 Оставить отзыв",
    )
    return generate_reply_keyboard_menu_buttons(2, commands, markup)
