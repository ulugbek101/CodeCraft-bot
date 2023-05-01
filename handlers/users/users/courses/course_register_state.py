from aiogram import types
from aiogram.contrib.middlewares.fsm import FSMContext
from aiogram.types import Message, CallbackQuery

from keyboards.default.cancel_btn import generate_cancel_btn
from keyboards.default.users.contact_send_menu import generate_send_contact_menu
from keyboards.default.main_menu import generate_main_menu
from loader import dp, db, bot
from tools.permissions import private_chat
from states.users.courses import CourseRegisterState
from data.config import ADMINS


@dp.callback_query_handler(lambda call: "course-register" == call.data.split(":")[0])
async def course_state_start(call: CallbackQuery, state: FSMContext):
    if private_chat(call.message):
        await CourseRegisterState.course.set()
        await state.update_data(course=db.get_course(int(call.data.split(":")[1]))[1])
        await CourseRegisterState.next()
        await call.message.answer("<b>Введите свое полное имя, например: Умаралиев Улугбек</b>",
                                  reply_markup=generate_cancel_btn())
        await call.message.delete()


@dp.message_handler(state=CourseRegisterState.fullname)
async def save_fullname(message: Message, state: FSMContext):
    await state.update_data(fullname=message.text)
    await CourseRegisterState.next()
    await message.answer("<b>Отправьте номер своего телефона</b>", reply_markup=generate_send_contact_menu())


@dp.message_handler(state=CourseRegisterState.tel, content_types=types.ContentType.CONTACT)
@dp.message_handler(state=CourseRegisterState.tel)
async def save_tel(message: Message, state: FSMContext):
    if private_chat(message):
        if message.contact:
            await state.update_data(tel=message.contact.phone_number)
        else:
            await state.update_data(tel=message.text)
        try:
            await state.update_data(username=message.from_user.username)
        except:
            await state.update_data(username='-')
        data = await state.get_data()
        msg = f"===== Новый студент =====\n\n"
        msg += f"Ф.И.О: <b>{data['fullname']}</b>\n"
        msg += f"Курс: <b>{data['course']}</b>\n"
        msg += f"Тел: <b>{data['tel']}</b>\n"
        msg += f"Username: <b>{'@' + data['username'] if data['username'] != '-' else '-'}</b>\n"
        for admin in ADMINS:
            try:
                await bot.send_message(admin, msg)
            except:
                pass
        await state.finish()
        await message.answer(
            "<b>Ваши данные приняты, в скором времени администрация свяжется с вами для уточнения деталей 😉</b>",
            reply_markup=generate_main_menu())
