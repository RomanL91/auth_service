from datetime import datetime

from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from core import Base
from core.function_utils import get_current_time


class UserT(Base):
    firt_name: Mapped[str] = mapped_column(
        String(100),
    )
    last_name: Mapped[str] = mapped_column(
        String(100),
    )
    update_at: Mapped[datetime] = mapped_column(
        default=get_current_time,
        nullable=True,
    )
    last_login: Mapped[datetime] = mapped_column(
        nullable=True,
    )
    active: Mapped[bool] = mapped_column(
        Boolean(),
        default=True,
    )
    external_id: Mapped[str] = mapped_column(
        String(150),
        nullable=True,
    )

    def __str__(self):
        return f"id={self.id}, name={self.firt_name!r})"

    def __repr__(self):
        return str(self)
