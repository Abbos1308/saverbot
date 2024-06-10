from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from utils.db_api.sqlite import Database
from data import config

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db = Database(dbname="saverbot_db", user="saverbot_db_user", password="QgLON8WtRCH5WZIcrLgZkme0EFZCumtv", host="dpg-cpj7926ct0pc7384ua1g-a.oregon-postgres.render.com", port="5432")
