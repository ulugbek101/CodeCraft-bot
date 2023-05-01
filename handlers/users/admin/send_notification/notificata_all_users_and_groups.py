from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters import Text

from loader import dp, db, bot
from tools.permissions import private_chat, is_admin
from states.admin.notification import NotificationState
from keyboards.default.cancel_btn import generate_cancel_btn
from keyboards.default.admin.admin_menu import generate_admin_main_menu


@dp.message_handler(Text("📣📃 Подать объявление"))
async def notification_state_start(message: Message):
    if private_chat(message) and is_admin(message.from_user.id):
        await NotificationState.body.set()
        await message.answer("<b>Создайте либо перешлите объявление</b>", reply_markup=generate_cancel_btn())
        # users = db.get_subscribed_users()
        # groups = db.get_groups()


@dp.message_handler(state=NotificationState.body, content_types='photo')
@dp.message_handler(state=NotificationState.body)
async def save_notification(message: Message, state: FSMContext):
    users = db.get_subscribed_users()
    groups = db.get_groups()
    if message.photo:
        await message.photo[-1].download(destination_file='media/notification-photos/photo.jpg')
        async with state.proxy() as data:
            data['body'] = message.caption
            text = data['body']
        for user in users:
            try:
                with open(file='media/notification-photos/photo.jpg', mode='rb') as photo:
                    await bot.send_photo(chat_id=user[1], photo=photo, caption=text)
            except:
                pass
        for group in groups:
            with open(file='media/notification-photos/photo.jpg', mode='rb') as photo:
                try:
                    msg = await bot.send_photo(chat_id=group[1], photo=photo, caption=text)
                    await bot.pin_chat_message(chat_id=group[1], message_id=msg.message_id)
                except:
                    pass
    else:
        async with state.proxy() as data:
            data['body'] = message.text
            text = data['body']
        for user in users:
            try:
                await bot.send_message(chat_id=user[1], text=text)
            except:
                pass
        for group in groups:
            try:
                msg = await bot.send_message(chat_id=group[1], text=text)
                await bot.pin_chat_message(chat_id=group[1], message_id=msg.message_id)
            except:
                pass
    await state.finish()
    await message.answer("<b>Объвление успешно опубликовано в группах и отпралено всем подписчикам ✔</b>",
                         reply_markup=generate_admin_main_menu())
