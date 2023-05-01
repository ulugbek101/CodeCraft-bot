from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery

from loader import dp, db
from tools.permissions import is_admin, private_chat
from keyboards.default.admin import admin_menu
from keyboards.inline.admin import open_lessons_delete_inline_menu


@dp.message_handler(Text("🗑 Удалить назначенный урок"))
async def open_lesson_remove_start(message: Message):
    if is_admin(message.from_user.id) and private_chat(message):
        lessons = db.get_open_lessons()
        if len(lessons) > 0:
            await message.answer("<b>Выберите одно из этих открытых уроков чтобы удалить</b>",
                                 reply_markup=open_lessons_delete_inline_menu.generate_lessons_remove_menu(
                                     [lesson for lesson in lessons]))

        else:
            await message.answer("<b>Пока нет запланированных открытых уроков 🧐</b>",
                                 reply_markup=admin_menu.generate_admin_main_menu())


@dp.callback_query_handler(lambda call: "open-lesson-remove" == call.data.split(":")[0])
async def remove_open_lesson(call: CallbackQuery):
    table_id = int(call.data.split(":")[1])
    lesson = db.get_open_lesson(table_id)[1]
    db.drop_open_lesson(lesson)
    db.remove_from_open_lessons_list(lesson)
    await call.answer(f'Открытый урок "{lesson.replace("_", " ").upper()}" успешно удалён !', show_alert=True)
    await call.message.delete()




