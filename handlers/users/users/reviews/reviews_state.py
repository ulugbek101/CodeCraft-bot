from aiogram.contrib.middlewares.fsm import FSMContext

from data.config import ADMINS
from keyboards.default.cancel_btn import generate_cancel_btn
from states.users.reviews import ReviewState
from aiogram.dispatcher.filters import Text
from loader import dp, bot, db
from aiogram.types import Message, CallbackQuery
from tools.permissions import private_chat
from keyboards.default.main_menu import generate_main_menu
from keyboards.inline.admin.review_answer import generate_review_answer_keyboard


@dp.message_handler(Text("📝 Оставить отзыв"))
async def review_state_start(message: Message):
    if private_chat(message):
        await ReviewState.body.set()
        await message.answer("<b>Здравствуйте ещё раз, тут вы можете написать свой отзыв, предпочтения, пожелания. "
                             "Мы будем очень рады узнать ваше мнение 😉</b>",
                             reply_markup=generate_cancel_btn())


@dp.message_handler(state=ReviewState.body)
async def send_review(message: Message, state: FSMContext):
    await state.update_data(body=message.text)
    review = f"<b>Отзыв/Пожелание:</b>\n\n<b>От:</b> <i>{message.from_user.full_name}</i> | {'@' + message.from_user.username if message.from_user.username else '---'}\n"
    review += f"{'-' * 20}\n<i>{message.text}</i>\n{'-' * 20}"
    user_id = int(db.get_user(message.from_user.id)[0])
    for admin in ADMINS:
        try:
            await bot.send_message(admin, review,
                                   reply_markup=generate_review_answer_keyboard("📝 Ответить ...", user_id, 0))
        except:
            pass
    await state.finish()
    await message.answer("<b>Ваш отзыв/пожелание отправлен(о) администрации, в скором времени мы вам ответим 😉</b>",
                         reply_markup=generate_main_menu())
