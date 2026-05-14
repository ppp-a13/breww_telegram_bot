from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message

from repositories.categories import CategoryRepository
from repositories.teas import TeaRepository
from repositories.user import UserRepository
from repositories.cart import CartRepository


class DatabaseSessionMiddleware(BaseMiddleware):
    def __init__(self, session_maker) -> None:
        self.session_maker = session_maker

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        async with self.session_maker() as session:
            data['user_repository'] = UserRepository(session=session)
            data['category_repository'] = CategoryRepository(session=session)
            data['tea_repository'] = TeaRepository(session=session)
            data['cart_repository'] = CartRepository(session=session)
            return await handler(event, data)