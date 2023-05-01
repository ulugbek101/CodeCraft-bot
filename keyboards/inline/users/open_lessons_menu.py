from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from tools.menu_generating import generate_inline_keyboard_menu_buttons


def generate_open_lessons_menu(open_lessons_list: tuple):
    markup = InlineKeyboardMarkup()
    return generate_inline_keyboard_menu_buttons(2, open_lessons_list, markup, "open-lesson-register")
