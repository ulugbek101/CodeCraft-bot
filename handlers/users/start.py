from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp, db

from keyboards import default


@dp.message_handler(CommandStart())
async def show_main_menu(message: types.Message):
    if not message.chat.type == "supergroup":
        try:
            db.register_user(message.from_user.id, message.from_user.full_name, message.from_user.username)
        except:
            pass

        msg = f"""Здравствуйте!  {message.from_user.full_name} 🤗\n\n"""
        msg += """Добро пожаловать в чат-бот, который поможет вам оставить заявку на наши курсы программирования\n\n"""
        msg += """Для продолжения выберите пункт "Оставить заявку" из меню ниже."""
        with open('media/logo/logo_img.jpg', "rb") as photo:
            await message.answer_photo(photo, msg, reply_markup=default.main_menu.generate_main_menu())
