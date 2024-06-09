import logging

from aiogram import Dispatcher , types

from data.config import ADMINS


async def on_startup_notify(dp: Dispatcher):
    for admin in ADMINS:
        try:
            await dp.bot.send_message(admin, "Bot ishga tushdi!")

        except Exception as err:
            logging.exception(err)

async def on_shutdown_notify(dp: Dispatcher):
    file = types.InputFile("main.db")
    await dp.bot.send_document(ADMINS[0],file)
    for admin in ADMINS:
        try:
            
            await dp.bot.send_message(admin, "Bot o'chdi! Xabar oling")

        except Exception as err:
            logging.exception(err)

