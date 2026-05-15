from aiogram import Router, types
from aiogram.filters import Command

from keyboards.menu import main_menu_keyboard
from repositories.user import UserRepository

router = Router()


@router.message(Command('start'))
async def start_bot(message: types.Message, user_repository: UserRepository):
    await user_repository.create_or_update_user(
        message.from_user.id,
        message.from_user.full_name,
        message.from_user.username
    )
    await message.answer(
        f'Привет, {message.from_user.full_name} 👋\n\nДобро пожаловать в <b>BREWW</b> — магазин чая для тех, кто ценит удовольствие',
        reply_markup=main_menu_keyboard(),
        parse_mode='html'
    )
