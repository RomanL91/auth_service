from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from core import Base


class User(Base):
    username: Mapped[str] = mapped_column(String(20), unique=True)
    password: Mapped[str] = mapped_column(String(20), nullable=False)

    email: Mapped[str] = mapped_column(String(), nullable=True)
    active: Mapped[bool] = mapped_column(Boolean(), default=True)

    def __str__(self):
        return f"id={self.id}, username={self.username!r})"

    def __repr__(self):
        return str(self)
