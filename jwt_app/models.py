import uuid

from datetime import datetime
from enum import Enum as PyEnum

from sqlalchemy import ForeignKey, Enum, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core import Base
from core.function_utils import get_current_time


class TokenTypeEnum(str, PyEnum):
    ACCESS = "access_token"
    REFRESH = "refresh_token"


class JWToken(Base):
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("userts.id", ondelete="SET NULL"),
        nullable=True,
    )
    issued_at: Mapped[datetime] = mapped_column(
        default=get_current_time,
        nullable=False,
    )
    expires_at: Mapped[datetime] = mapped_column(
        nullable=False,
    )
    token_type: Mapped[TokenTypeEnum] = mapped_column(
        Enum(TokenTypeEnum),
        nullable=False,
    )
    token: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )
    revoked: Mapped[bool] = mapped_column(
        default=False,
        nullable=False,
    )
    user: Mapped["UserT"] = relationship(  # type: ignore
        "UserT",
        back_populates="tokens",
    )
