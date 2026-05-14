import os
from dotenv import load_dotenv
from aiogram.filters import BaseFilter
from aiogram import types

load_dotenv()
ADMIN_IDS = list(map(int, os.getenv('ADMIN_IDS', '').split(',')))

class IsAdmin(BaseFilter):
    async def __call__(self, message: types.Message | types.CallbackQuery) -> bool:
        if isinstance(message, types.CallbackQuery):
            user_id = message.from_user.id
        else:
            user_id = message.from_user.id
        return user_id in ADMIN_IDS