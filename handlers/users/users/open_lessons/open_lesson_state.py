from aiogram.contrib.middlewares.fsm import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery
from aiogram import types

from loader import dp, db
from tools.permissions import private_chat
from keyboards import default
from keyboards import inline
from states.users.open_lessons import OpenLessonRegisterState


@dp.message_handler(Text("🖋📄 Записаться на пробный урок"))
async def open_lesson_state_manage(message: Message):
    if private_chat(message):
        open_lessons = db.get_open_lessons()
        if len(open_lessons) > 0:
            i = 0
            msg = f"<b>У нас запланированы следующие пробные уроки в ближащие даты</b>\n\n"
            for lesson in open_lessons:
                i += 1
                msg += f"{i}) {'-' * 20}\nНазвание открытого урока: <i>{lesson[1].replace('_', ' ').title()}</i>\n"
                msg += f"Дата проведения: <i>{lesson[2]}</i>\n\n"
            await message.answer(msg,
                                 reply_markup=inline.users.open_lessons_menu.generate_open_lessons_menu(
                                     tuple([lesson[:2] for lesson in open_lessons])
                                 ))
        else:
            await message.answer("<b>У нас пока нету запланированных пробных уроков 🤔</b>",
                                 reply_markup=default.main_menu.generate_main_menu())


@dp.callback_query_handler(lambda call: "open-lesson-register" == call.data.split(":")[0])
async def open_lesson_state_start(call: CallbackQuery, state: FSMContext):
    table_name = db.get_open_lesson(int(call.data.split(":")[1]))[1]
    await OpenLessonRegisterState.full_name.set()
    await state.update_data(table_name=table_name)
    await call.message.answer("<b>Введите ваше полное имя</b>", reply_markup=default.cancel_btn.generate_cancel_btn())
    await call.message.delete()


@dp.message_handler(state=OpenLessonRegisterState.full_name)
async def save_fullname(message: Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    await OpenLessonRegisterState.next()
    await message.answer("<b>Отправьте свой номер телефона</b>",
                         reply_markup=default.users.contact_send_menu.generate_send_contact_menu())


@dp.message_handler(state=OpenLessonRegisterState.tel)
@dp.message_handler(state=OpenLessonRegisterState.tel, content_types=types.ContentType.CONTACT)
async def save_tel(message: Message, state: FSMContext):
    if message.contact:
        await state.update_data(tel=message.contact.phone_number)
    else:
        await state.update_data(tel=message.text)
    try:
        await state.update_data(user_name=message.from_user.username)
    except:
        await state.update_data(user_name='-')
    await state.update_data(chat_id=message.from_user.id)
    async with state.proxy() as data:
        db.register_student_to_open_lesson(
            table_name=data['table_name'],
            chat_id=data['chat_id'],
            tel=data['tel'],
            full_name=data['full_name'],
            user_name=data['user_name']
        )
    await state.finish()
    await message.answer(
        "<b>Ваши данные приняты, в скором времени администрация свяжется с вами для уточнения деталей 😉</b>",
        reply_markup=default.main_menu.generate_main_menu())
