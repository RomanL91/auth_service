import uuid

from sqlalchemy import String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core import Base


class SocialAccount(Base):
    provider: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )
    provider_user_id: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(
            "userts.id",
            ondelete="SET NULL",
        ),
        nullable=True,
    )
    user: Mapped["UserT"] = relationship(  # type: ignore
        "UserT",
        back_populates="social_accounts",
    )

    def __str__(self):
        return f"id={self.id}, provider={self.provider!r}, user={self.user!r}"

    def __repr__(self):
        return str(self)
