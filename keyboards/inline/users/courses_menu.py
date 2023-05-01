from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from tools.menu_generating import generate_inline_keyboard_menu_buttons


def generate_courses_menu(courses: tuple | list):
    markup = InlineKeyboardMarkup()
    return generate_inline_keyboard_menu_buttons(2, courses, markup, prefix=f"course-info")


def generate_register_to_course_menu(course_id: int):
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton(text=f"📝 Записаться на курс", callback_data=f"course-register:{course_id}")
    )
    return markup
