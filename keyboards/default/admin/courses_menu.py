from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from tools.menu_generating import generate_reply_keyboard_menu_buttons, return_main_menu


def generate_courses_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    commands = (
        "🖋 Добавить курс",
        "🗑 Удалить курс"
    )
    markup = generate_reply_keyboard_menu_buttons(2, commands, markup)
    return return_main_menu(markup)
