from aiogram.types import ReplyKeyboardMarkup
from tools.menu_generating import generate_reply_keyboard_menu_buttons


def generate_admin_main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    commands = (
        "📃 Статистика",
        "📝 Пробные уроки",
        "📚 Курсы",
        # "👨‍🎓 Группы",
        "📣📃 Подать объявление"
    )
    return generate_reply_keyboard_menu_buttons(2, commands, markup)
