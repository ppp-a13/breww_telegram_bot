from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from database.models.cart import CartItem


class CartRepository:
    def __init__(self, session: AsyncSession):
        self.__session = session

    async def add_item(self, user_id: int, tea_id: int):
        statement = select(CartItem).where(
            CartItem.user_id == user_id,
            CartItem.tea_id == tea_id
        )
        item = await self.__session.scalar(statement)

        if item:
            item.quantity += 1
        else:
            item = CartItem(user_id=user_id, tea_id=tea_id, quantity=1)
            self.__session.add(item)

        await self.__session.commit()

    async def get_cart(self, user_id: int):
        statement = select(CartItem).where(CartItem.user_id == user_id)
        return await self.__session.scalars(statement)

    async def remove_item(self, user_id: int, tea_id: int):
        statement = delete(CartItem).where(
            CartItem.user_id == user_id,
            CartItem.tea_id == tea_id
        )
        await self.__session.execute(statement)
        await self.__session.commit()

    async def clear_cart(self, user_id: int):
        statement = delete(CartItem).where(CartItem.user_id == user_id)
        await self.__session.execute(statement)
        await self.__session.commit()
