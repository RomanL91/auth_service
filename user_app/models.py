from datetime import datetime

from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

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
    client_uuid: Mapped[str] = mapped_column(
        UUID,
        nullable=True,
    )
    # внешний ключ связи 1-к-1 на номера телефонов
    phone_number_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("phonenumbers.id"),
    )
    phone_number: Mapped["PhoneNumber"] = relationship(  # type: ignore
        "PhoneNumber", 
        uselist=False, 
        back_populates="user", 
        cascade="all",
    )
    emails: Mapped[list["Email"]] = relationship(  # type: ignore
        "Email",
        back_populates="user",
        cascade="all",
    )
    social_accounts: Mapped[list["SocialAccount"]] = relationship(  # type: ignore
        "SocialAccount",
        back_populates="user",
        cascade="all",
    )
    tokens: Mapped[list["JWToken"]] = relationship(  # type: ignore
        "JWToken",
        back_populates="user",
        cascade="all",
    )

    def __str__(self):
        return f"id={self.id}, name={self.firt_name!r})"

    def __repr__(self):
        return str(self)
