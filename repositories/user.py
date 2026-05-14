from sqlalchemy import select
from database.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.__session = session

    async def get_user_by_telegram_id(self, telegram_id: int):
        statement = select(User).where(User.telegram_id == telegram_id)

        return await self.__session.scalar(statement)

    async def create_or_update_user(self, telegram_id: int, fullname: str, username: str):
        user = await self.get_user_by_telegram_id(telegram_id)

        if not user:
            await self.create_user(telegram_id, fullname, username)
        else:
            user.fullname = fullname
            user.username = username

        await self.__session.commit()

    async def create_user(self, telegram_id: int, fullname: str, username: str):
        user = User(telegram_id=telegram_id, fullname=fullname, username=username)
        self.__session.add(user)

    async def update_balance(self, telegram_id: int, amount: int):

        statement = update(User).where(User.telegram_id == telegram_id).values(
            balance=User.balance + amount
        )
        await self.__session.execute(statement)
        await self.__session.commit()

    async def get_by_telegram_id(self, telegram_id: int):
        statement = select(User).where(User.telegram_id == telegram_id)
        return await self.__session.scalar(statement)