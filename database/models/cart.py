from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped

from database.models import BaseModel


class CartItem(BaseModel):
    __tablename__ = 'cart_items'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    tea_id: Mapped[int] = mapped_column(ForeignKey('teas.id'))
    quantity: Mapped[int] = mapped_column(default=1)
