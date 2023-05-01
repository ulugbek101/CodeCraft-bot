from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def generate_lessons_remove_menu(lessons: list):
    markup = InlineKeyboardMarkup()
    in_row = 2
    start = 0
    end = in_row
    rows = len(lessons) // 2
    if len(lessons) % 2 != 0:
        rows += 1
    for _ in range(rows):
        btns = []
        for id_, name, datetime in lessons[start:end]:
            btns.append(
                InlineKeyboardButton(
                    text=name.replace("_", " ").upper(),
                    callback_data=f"open-lesson-remove:{id_}"
                )
            )
        markup.row(*btns)
        start = end
        end += in_row
    return markup
