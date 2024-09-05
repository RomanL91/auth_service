from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core import Base


class PhoneNumber(Base):
    phone_number: Mapped[str] = mapped_column(
        String(11), 
        nullable=True,
    )
    user: Mapped["UserT"] = relationship(  # type: ignore
        "UserT",
        back_populates="phone_number",
    )
    sms_codes: Mapped[list["SMSCode"]] = relationship(  # type: ignore
        "SMSCode",
        back_populates="phone_number",
    )

    def __str__(self) -> str:
        return f"id={self.id} phone num={self.phone_number!r}"

    def __repr__(self) -> str:
        return str(self)
