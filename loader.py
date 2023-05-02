from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from data import config
from utils.db_api.database import Database

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db = Database(
    db_name="railway",
    db_password="wnmDJ7M2JSyouozWmpz4",
    db_user="root",
    db_port=5440,
    db_host="containers-us-west-39.railway.app"
)
