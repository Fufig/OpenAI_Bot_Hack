import asyncio
import os
from dotenv import load_dotenv
load_dotenv()

from aiogram import Bot, Dispatcher

from bot.app.handlers import router
from bot.app.database.models import async_main



async def main():
    await async_main()
    bot = Bot(token=os.getenv('TOKEN'))
    dp = Dispatcher()
    dp.include_router(router)
    print('Поехало!')
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except:
        print('Бот выключился, RIP, gg')
