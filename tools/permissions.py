from environs import Env
from aiogram.types import Message


env = Env()
env.read_env()

ADMINS = env.list("ADMINS")


def is_admin(chat_id: int):
    for admin in ADMINS:
        if int(admin) == chat_id:
            return True
    return False


def private_chat(message: Message):
    if not message.chat.type == "supergroup":
        return True
    else:
        return False


