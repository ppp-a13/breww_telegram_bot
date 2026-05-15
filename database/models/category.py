from sqlalchemy.orm import mapped_column, Mapped

from database.models import BaseModel


class Category(BaseModel):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    description: Mapped[str]
