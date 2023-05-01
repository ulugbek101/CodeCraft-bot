from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery

from loader import dp, db
from tools.permissions import private_chat, is_admin
from keyboards.default import admin
from keyboards.inline.admin import course_delete_menu


@dp.message_handler(Text("🗑 Удалить курс"))
async def course_delete_state_start(message: Message):
    if private_chat(message) and is_admin(message.from_user.id):
        if len(db.get_courses()) == 0:
            await message.answer("<b>Пока нет доступных курсов 🧐</b>",
                                 reply_markup=admin.admin_menu.generate_admin_main_menu())
        else:
            await message.answer("<b>Нажмите на курс, которую хотите удалить 🗑</b>",
                                 reply_markup=course_delete_menu.generate_course_delete_menu())


@dp.callback_query_handler(lambda call: "course-delete" == call.data.split(":")[0])
async def course_delete(call: CallbackQuery):
    if private_chat(call.message) and is_admin(call.message.chat.id):
        course_id = call.data.split(":")[1]
        course = db.get_course(int(course_id))[1]
        db.remove_from_courses_list(int(call.data.split(":")[1]))
        await call.answer(f'Курс "{course}" успешно удалён !', show_alert=True)
        await call.message.delete()
