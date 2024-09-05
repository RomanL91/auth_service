import uuid

from sqlalchemy import String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core import Base


class SMSCode(Base):
    code: Mapped[str] = mapped_column(
        String(6),
        nullable=False,
    )
    is_used: Mapped[bool] = mapped_column(
        default=True,
    )
    phone_number_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("phonenumbers.id"),
    )
    phone_number: Mapped["PhoneNumber"] = relationship(  # type: ignore
        "PhoneNumber",
        back_populates="sms_codes",
    )
