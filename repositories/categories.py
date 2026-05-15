from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models.category import Category


class CategoryRepository:
    def __init__(self, session: AsyncSession):
        self.__session = session

    async def get_list(self):
        statement = select(Category).order_by(Category.name)
        return await self.__session.scalars(statement)

    async def get_by_id(self, category_id: int):
        statement = select(Category).where(Category.id == category_id)
        return await self.__session.scalar(statement)
