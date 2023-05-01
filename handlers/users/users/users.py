from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery

from keyboards.default import users
from keyboards.default.users import settings_menu
from keyboards.inline.users.courses_menu import generate_courses_menu, generate_register_to_course_menu
from loader import dp, db
from tools.permissions import private_chat
from data.config import branches

from geopy.distance import geodesic


@dp.message_handler(Text("📞 Наши контакты"))
async def send_contacts(message: Message):
    if private_chat(message):
        msg = " 👤 <b>Админ: @CodeCraftedu</b>\n"
        msg += '📣 <b>Телеграм канал: <a href="https://t.me/art_of_coding">CodeCraft</a></b>\n'
        msg += "📞 <b>Телефон админа: \n" \
               "    1. +998903005500\n" \
               "    2. +998995845551</b>\n"
        await message.answer(msg)


@dp.message_handler(Text("⚙️ Настройки"))
async def manage_settings(message: Message):
    if private_chat(message):
        is_subscribed = db.get_user(chat_id=message.from_user.id)[4]
        await message.answer("<b>Нажмите на кнопку чтобы включить/отключить уведомления от бота</b>",
                             reply_markup=users.settings_menu.generate_settings_menu(is_subscribed))


@dp.message_handler(Text("🔍 Узнать о курсах"))
async def show_courses_menu(message: Message):
    if private_chat(message):
        await message.answer(
            "<b>У нас есть следующие курсы 👇, выберите один, чтобы увидеть подробную информацию об этом курсе</b>",
            reply_markup=generate_courses_menu(tuple([course[:2] for course in db.get_courses()])))


@dp.message_handler(content_types='location')
async def send_location(message: Message):
    if private_chat(message):
        await message.answer(f"<b>В настоящее время у нас {len(branches)} филиала</b>")
        for branch in branches:
            await message.answer(f"<b>Расстяние с вашего местоположения до этого 👇 филиала, составляет "
                                 f"{round(geodesic((message.location.latitude, message.location.longitude), branch).km, 2)} "
                                 f"km. </b>")
            await message.answer_location(
                latitude=branch[0],
                longitude=branch[1]
            )


@dp.callback_query_handler(lambda call: "course-info" == call.data.split(":")[0])
async def show_course_info(call: CallbackQuery):
    if private_chat(call.message):
        course_id = int(call.data.split(":")[1])
        course = db.get_course(course_id)
        with open(file=f'{course[2]}', mode='r', encoding='UTF-8') as file:
            text = file.read()
        with open(file=f'{course[3]}', mode='rb') as photo:
            await call.message.answer_photo(photo=photo, caption=text,
                                            reply_markup=generate_register_to_course_menu(course_id=course_id))
        await call.message.delete()


@dp.message_handler(Text("❌📩 Выключить уведомления"))
@dp.message_handler(Text("✅📩 Включить уведомления"))
async def notification_manage(message: Message):
    if private_chat(message):
        subscription_state = db.get_user(message.from_user.id)[4]
        print(subscription_state)
        db.update_user_subscription_state(is_subscribed=0 if int(subscription_state) == 1 else 1,
                                          chat_id=message.from_user.id)
        await message.answer(f"<b>Уведомления <i>{'включены' if subscription_state == 0 else 'отключены'}</i></b>",
                             reply_markup=settings_menu.generate_settings_menu(
                                 user_subscribed_state=1 if subscription_state == 0 else 0
                             ))
