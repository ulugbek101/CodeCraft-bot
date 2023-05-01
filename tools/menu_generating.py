from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


def generate_inline_keyboard_menu_buttons(in_row: int, items: tuple, markup: InlineKeyboardMarkup, prefix: str):
    in_row = in_row
    start = 0
    end = in_row
    rows = len(items) // 2
    if len(items) % 2 != 0:
        rows += 1
    for _ in range(rows):
        btns = []
        for id_, name in items[start:end]:
            btns.append(
                InlineKeyboardButton(text=name, callback_data=f'{prefix}:{id_}')
            )
        markup.row(*btns)
        start = end
        end += in_row
    return markup


def generate_reply_keyboard_menu_buttons(in_row: int, commands: tuple, markup: ReplyKeyboardMarkup):
    in_row = in_row
    start = 0
    end = in_row
    rows = len(commands) // in_row
    if len(commands) % in_row != 0:
        rows += 1
    for _ in range(rows):
        btns = []
        for command in commands[start:end]:
            btns.append(
                KeyboardButton(text="📌 Локация", request_location=True) if command == "📌 Локация" else KeyboardButton(
                    text=command)
            )
        markup.row(*btns)
        start = end
        end += in_row
    return markup


def return_main_menu(markup: ReplyKeyboardMarkup):
    markup.row(
        KeyboardButton(text="🔙 Главное меню")
    )
    return markup
