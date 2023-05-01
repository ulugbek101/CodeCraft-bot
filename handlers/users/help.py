from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = ("<b>Команды: </b>",
            "<b>/start - Активировать бота</b>",
            "<b>/help - Помощь</b>")
    
    await message.answer("\n".join(text))