from aiogram.types import InlineKeyboardMarkup
from tools.menu_generating import generate_inline_keyboard_menu_buttons

from loader import db


def generate_group_delete_menu():
    markup = InlineKeyboardMarkup()
    groups = tuple([group[1:3] for group in db.get_groups()])
    return generate_inline_keyboard_menu_buttons(
        in_row=2,
        items=groups,
        markup=markup,
        prefix="group-delete"
    )

