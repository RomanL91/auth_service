import uuid

from sqlalchemy import String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core import Base


class Email(Base):
    email: Mapped[str] = mapped_column(
        String,
        nullable=True,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("userts.id"),
    )
    user: Mapped["UserT"] = relationship(  # type: ignore
        "UserT",
        back_populates="emails",
    )

    def __str__(self) -> str:
        return f"id={self.id} email={self.email!r}"

    def __repr__(self) -> str:
        return str(self)
