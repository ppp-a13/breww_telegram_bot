import asyncio
from aiogram import Bot, Dispatcher, Router, types
from handlers import register_routes
from database.models import BaseModel
from middlewares import register_middlewares
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
import os
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')


async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    engine = create_async_engine(
        url = 'sqlite+aiosqlite:///breww_shop.db'
    )
    session_maker = async_sessionmaker(engine, expire_on_commit=False)


    register_middlewares(dp, session_maker)
    register_routes(dp)

    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('БОТ ОСТАНОВЛЕН')