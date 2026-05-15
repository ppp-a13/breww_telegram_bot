from aiogram import Dispatcher

from middlewares.session import DatabaseSessionMiddleware


def register_middlewares(dp: Dispatcher, session_maker):
    dp.update.middleware(DatabaseSessionMiddleware(session_maker))
