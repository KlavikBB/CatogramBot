#!/root/py_proj/cat_bot/venv/bin/python3

import os
import logging
from dotenv import load_dotenv

import asyncio
from aiogram import Bot, Dispatcher

from app.handlers import router
from app.database.models import async_main

load_dotenv()

bot = Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))
dp = Dispatcher()


async def main():
    await async_main()
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())