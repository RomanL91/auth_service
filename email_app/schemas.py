from typing import Annotated
from annotated_types import MinLen, MaxLen
from pydantic import BaseModel, EmailStr, ConfigDict, HttpUrl, UUID4

from social_acc_app.schemas import GoogleUserInfo
from user_app.schemas import SaveUserSchema


class SaveEmailSchema(BaseModel):
    id: UUID4


class EmailSchema(BaseModel):
    email: EmailStr
    user_id: UUID4

    @classmethod
    def convert_data(
        cls, google_user: GoogleUserInfo, user: SaveUserSchema
    ) -> "EmailSchema":
        return cls(
            email=google_user.email,
            user_id=user.id,
        )
