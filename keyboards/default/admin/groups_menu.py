from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from tools.menu_generating import generate_reply_keyboard_menu_buttons, return_main_menu


def generate_groups_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    commands = (
        "🖋 Добавить группу",
        "🗑 Удалить группу"
    )
    return return_main_menu(generate_reply_keyboard_menu_buttons(2, commands, markup))
