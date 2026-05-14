from aiogram import types
from aiogram.filters import Filter

from keyboards.catalog import BuyTeaCallBackData
from repositories.teas import TeaRepository
from repositories.user import UserRepository


class FilterUserCanBuyTea(Filter):
    async def __call__(
            self,
            callback: types.CallbackQuery,
            tea_repository: TeaRepository,
            user_repository: UserRepository
    ):
        try:
            buy_data = BuyTeaCallBackData.unpack(callback.data)
        except Exception:
            return False

        tea_id = int(callback.data.split(':')[-1])

        tea = await tea_repository.get_tea_by_id(tea_id)
        user = await user_repository.get_user_by_telegram_id(callback.from_user.id)

        if tea is None or user is None:
            return False

        if user.balance < tea.price:
            await callback.answer('Недостаточно монет!', show_alert=True)
            return False

        return True