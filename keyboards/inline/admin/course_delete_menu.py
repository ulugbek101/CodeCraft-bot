from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tools.menu_generating import generate_inline_keyboard_menu_buttons
from loader import db


def generate_course_delete_menu():
    markup = InlineKeyboardMarkup()
    print(tuple([course for course in db.get_courses()]))
    return generate_inline_keyboard_menu_buttons(2, tuple([course[0:2] for course in db.get_courses()]), markup,
                                                 prefix="course-delete")
