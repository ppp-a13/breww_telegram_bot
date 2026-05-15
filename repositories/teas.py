from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models.tea import Tea


class TeaRepository:
    def __init__(self, session: AsyncSession):
        self.__session = session

    async def get_teas_by_category_id(self, category_id):
        statement = select(Tea).where(Tea.category_id == category_id, Tea.quantity > 0).order_by(Tea.name)
        result = await self.__session.scalars(statement)
        return result.all()

    async def get_tea_by_id(self, tea_id):
        statement = select(Tea).where(Tea.id == tea_id)
        return await self.__session.scalar(statement)

    async def get_all_teas(self):
        statement = select(Tea).order_by(Tea.category_id, Tea.name)
        return await self.__session.scalars(statement)

    async def add_tea(self, name, description, price, category_id, quantity, photo_id=None):
        tea = Tea(
            name=name,
            description=description,
            price=price,
            category_id=category_id,
            quantity=quantity,
            photo_id=photo_id
        )
        self.__session.add(tea)
        await self.__session.commit()
        return tea

    async def update_tea_fields(self, tea_id, field, value):
        statement = select(Tea).where(Tea.id == tea_id)
        tea = await self.__session.scalar(statement)
        setattr(tea, field, value)
        await self.__session.commit()

    async def delete_tea(self, tea_id):
        statement = select(Tea).where(Tea.id == tea_id)
        tea = await self.__session.scalar(statement)
        await self.__session.delete(tea)
        await self.__session.commit()

    async def get_all_teas_by_category(self, category_id: int):
        statement = select(Tea).where(Tea.category_id == category_id).order_by(Tea.name)
        result = await self.__session.scalars(statement)
        return result.all()
