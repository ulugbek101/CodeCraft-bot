from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from tools.menu_generating import return_main_menu


def generate_settings_menu(user_subscribed_state: int):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(
        KeyboardButton(text="✅📩 Включить уведомления" if user_subscribed_state == 0 else "❌📩 Выключить уведомления")
    )
    return return_main_menu(markup)
