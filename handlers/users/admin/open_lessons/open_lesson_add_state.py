from aiogram.dispatcher.filters.builtin import Text
from aiogram.types import Message
from aiogram.contrib.middlewares.fsm import FSMContext

from loader import dp, db
from states.admin.open_lessons import OpenLessonState
from tools.permissions import is_admin, private_chat
from keyboards.default import cancel_btn
from keyboards.default.admin import admin_menu


@dp.message_handler(Text("🖋 Назначить открытый урок"), state=None)
async def open_lesson_state_start(message: Message):
    if private_chat(message) and is_admin(message.from_user.id):
        await OpenLessonState.name.set()
    await message.answer("<b>Введите название направления</b>", reply_markup=cancel_btn.generate_cancel_btn())


@dp.message_handler(state=OpenLessonState.name)
async def save_open_lesson_name(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await OpenLessonState.next()
    await message.answer("<b>Назначьте дату и время для открытого урока\nНапример: 15.06 11:30</b>",
                         reply_markup=cancel_btn.generate_cancel_btn())


@dp.message_handler(state=OpenLessonState.datetime)
async def save_open_lesson_datetime(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['datetime'] = message.text
        try:
            db.register_open_lesson(data['name'], data['datetime'])
            db.set_open_lesson(data['name'])
            await message.answer("<b>Открытый урок успешно добавлен !</b>",
                                 reply_markup=admin_menu.generate_admin_main_menu())
        except:
            await message.answer("<b>Что то пошло не так, проверьте правильность ввода и повторите заново !</b>",
                                 reply_markup=admin_menu.generate_admin_main_menu())
        await state.finish()
