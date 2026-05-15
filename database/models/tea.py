from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped

from database.models import BaseModel


class Tea(BaseModel):
    __tablename__ = 'teas'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    description: Mapped[str]
    price: Mapped[int]
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'))
    quantity: Mapped[int] = mapped_column(default=0)
    photo_id: Mapped[str | None] = mapped_column(default=None)
