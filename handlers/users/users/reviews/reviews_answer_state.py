from aiogram.types import CallbackQuery, Message
from aiogram.contrib.middlewares.fsm import FSMContext

from loader import dp, db, bot
from keyboards.inline import admin
from keyboards import default
from tools import permissions

from states.users.reviews_answer import ReviewsAnswerState


@dp.callback_query_handler(lambda call: "review-answer" == call.data.split(":")[0])
async def answer_review_state_start(call: CallbackQuery, state: FSMContext):
    if permissions.private_chat(call.message) and "0" == call.data.split(":")[1].split("-")[0]:
        await ReviewsAnswerState.body.set()
        await state.update_data(user_id=call.data.split(":")[1].split("-")[1])
        await call.message.delete()
        await call.message.answer("<b>Напишите свой ответ ...</b>",
                                  reply_markup=default.cancel_btn.generate_cancel_btn())


@dp.message_handler(state=ReviewsAnswerState.body)
async def send_review_answer(message: Message, state: FSMContext):
    await state.update_data(body=message.text)
    data = await state.get_data()
    chat_id = db.get_user_by_id(data['user_id'])[1]
    msg = "----- <b>Получен ответ на ваш(е) отзыв/пожелание</b> -----\n\n"
    msg += "<b>От:</b> <i>Администрация CodeCraft</i>\n"
    msg += f"{'-' * 20}\n<i>{data['body']}</i>\n{'-' * 20}"
    try:
        await bot.send_message(chat_id, msg)
    except:
        pass
    await message.answer("<i>Ответ отправлен !</i>", reply_markup=default.main_menu.generate_main_menu())
    await state.finish()
