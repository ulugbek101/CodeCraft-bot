from aiogram.types import Message

from loader import dp, bot
from tools.permissions import is_admin


@dp.message_handler(commands='id')
async def send_id_to_admin(message: Message):
    if is_admin(message.from_user.id):
        msg = f"Группа: {message.chat.title}\n" \
              f"ID группы: <code>{message.chat.id}</code>"
        await bot.send_message(chat_id=message.from_user.id, text=msg)
        await message.delete()
