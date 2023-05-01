from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def generate_courses_show_menu(courses: list):
    markup = InlineKeyboardMarkup()
    for course in courses:
        markup.row(
            InlineKeyboardButton(text=course[1], callback_data=f'course-show:{course[0]}')
        )
    return markup


