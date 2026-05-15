from sqlalchemy import BigInteger
from sqlalchemy.orm import mapped_column, Mapped

from database.models import BaseModel


class User(BaseModel):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True)

    username: Mapped[str | None]
    fullname: Mapped[str]

    balance: Mapped[int] = mapped_column(default=0)

    @property
    def view_balance(self):
        return round(self.balance / 100, 4)
