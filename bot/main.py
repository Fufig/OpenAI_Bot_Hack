import asyncio
import os
from dotenv import load_dotenv
load_dotenv()

from aiogram import Bot, Dispatcher

from bot.app.handlers import router
from bot.app.database.models import async_main

from app.gpt.gpt_handler import load_context_files



async def main():
    await async_main()
    bot = Bot(token=os.getenv('TOKEN'))
    dp = Dispatcher()
    dp.include_router(router)

    load_context_files()
    print('Поехало!')
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
    # try:
    #     asyncio.run(main())
    # except:
    #     print('Бот выключился, RIP, gg')
