from aiogram.dispatcher.filters.builtin import Command, Text
from aiogram.types import Message, CallbackQuery

from loader import dp, db

from keyboards import default, inline
from tools.permissions import private_chat, is_admin
from tools.weekdays_converter import convert_weekdays

import csv


@dp.message_handler(Command("admin"))
async def show_main_menu(message: Message):
    if private_chat(message) and is_admin(message.from_user.id):
        await message.answer("<b>Вы вошли в административную часть ✅</b>",
                             reply_markup=default.admin.admin_menu.generate_admin_main_menu())


@dp.message_handler(Text("📝 Пробные уроки"))
async def manage_open_lessons(message: Message):
    if private_chat(message) and is_admin(message.from_user.id):
        if len(db.get_open_lessons()) > 0:
            msg = """=== <b>Активные пробные уроки</b> ==="""
            i = 0
            lessons = db.get_open_lessons()
            for lesson in lessons:
                i += 1
                msg += f"\n\n{i}) {'=' * 10}\n"
                msg += f"Открытый урок по: <b>{lesson[1].replace('_', ' ').capitalize()}</b>\n"
                msg += f"Дата и время проведения: <b>{lesson[2]}</b>\n"
                students = db.get_open_lesson_students(table_name=lesson[1])
                ix = 0
                for student in students:
                    ix += 1
                    msg += f"    {ix}) {'-'*10}\n    Ф.И.О: <b>{student[2]}</b>\n"
                    msg += f"    Username: <b>{student[3]}</b>\n"
                    msg += f"    Tel: <b>{student[4]}</b>\n"
            await message.answer(msg,
                                 reply_markup=default.admin.open_lessons_menu.generate_open_lessons_menu())
        else:
            await message.answer(
                '<b>Пока нет запланированных открытых уроков 🧐, но вы всегда можете назначить новый нажав по кнопке'
                '\n"🖋 Назначить открытый урок"</b>\n',
                reply_markup=default.admin.open_lessons_menu.generate_open_lessons_menu())


# @dp.message_handler(Text("👨‍🎓 Группы"))
# async def manage_groups(message: Message):
#     if private_chat(message) and is_admin(message.from_user.id):
#         groups = db.get_groups()
#         msg = f"<b>На данный момент бот зарегистрирован в {len(groups)} группах</b>"
#         i = 0
#         for group in groups:
#             i += 1
#             lesson_days = convert_weekdays([int(day) for day in group[3].split(",") if day.strip().isdigit()])
#             msg += f"\n\n{i}) {'='*10}\n"
#             msg += f"Группа: <i>{group[2]}</i>\n"
#             msg += f"ID группы: <code>{group[1]}</code>\n"
#             msg += f"Дни занятий: <i>{','.join(lesson_days)}</i>\n"
#             msg += f"Время занятий: <i>{group[4]}</i>"
#         await message.answer(f"<b>{msg}</b>",
#                              reply_markup=default.admin.groups_menu.generate_groups_menu())


@dp.message_handler(Text("📚 Курсы"))
async def manage_courses(message: Message):
    if private_chat(message) and is_admin(message.from_user.id):
        if len(db.get_courses()) > 0:
            msg1 = "<b>Доступные курсы</b>\n\n" \
                   "Нажмите на один из кнопок, чтобы посмотреть информацию о курсе"
            msg2 = ""
            i = 0
            for course in db.get_courses():
                i += 1
                msg2 += f"{i}) Курс: <b>{course[1]}</b>\n\n"
            await message.answer(msg1,
                                 reply_markup=default.admin.courses_menu.generate_courses_menu())
            await message.answer(msg2, reply_markup=inline.admin.courses_show_menu.generate_courses_show_menu(
                [course[0:2] for course in db.get_courses()]))
        else:
            await message.answer("<b>Пока нет доступных курсов 🧐</b>",
                                 reply_markup=default.admin.courses_menu.generate_courses_menu())


@dp.message_handler(Text("📃 Статистика"))
async def send_stats(message: Message):
    if private_chat(message) and is_admin(message.from_user.id):
        users = db.get_users()
        with open(file='media/stats/stats.csv', mode='w') as file:
            writer = csv.writer(file)
            writer.writerow(
                ('ID', 'Телеграм ID', 'Полное имя', 'Username', 'Подписка')
            )
        with open(file='media/stats/stats.csv', mode='a') as file:
            for user in users:
                writer = csv.writer(file)
                writer.writerow(
                    (str(user[0]), str(user[1]), str(user[2]), str(user[3]), str(user[4]))
                )
        with open(file='media/stats/stats.csv', mode='rb') as file:
            await message.answer_document(document=file, caption='Полная статистика пользователей')


@dp.callback_query_handler(lambda call: "course-show" == call.data.split(":")[0])
async def show_course_info(call: CallbackQuery):
    if private_chat(call.message) and is_admin(call.message.chat.id):
        course = db.get_course(int(call.data.split(":")[1]))
        chat_id = call.message.chat.id
        name = course[1].replace(" ", "_").lower()
        await call.message.delete()
        with open(file=f'media/courses-info/{name}.txt', mode='r', encoding='utf-8') as file:
            text = file.read()
        with open(file=f'media/courses-logo/{name}.jpg', mode='rb') as photo:
            await call.message.answer_photo(photo=photo, caption=text)


@dp.message_handler(Text("🔙 Главное меню"))
async def return_main_menu(message: Message):
    if private_chat(message) and is_admin(message.from_user.id):
        await message.answer("<b>Вы вернулись в главное меню ✔</b>",
                             reply_markup=default.admin.admin_menu.generate_admin_main_menu())
    elif not message.chat.type == "supergroup":
        await message.answer("<b>Вы вернулись в главное меню ✔</b>",
                             reply_markup=default.main_menu.generate_main_menu())
