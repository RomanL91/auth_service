from typing import Annotated
from annotated_types import MinLen, MaxLen
from pydantic import BaseModel, EmailStr, ConfigDict, HttpUrl, UUID4




class OAuth2GoogleUrl(BaseModel):
    url: HttpUrl


class CodeFromGoogle(BaseModel):
    code: str


class GoogleUserInfo(BaseModel):
    id: str
    email: EmailStr
    verified_email: bool
    name: str
    given_name: str
    family_name: str
    picture: HttpUrl


# from user_app.schemas import SaveUserSchema
# from email_app.schemas import SaveEmailSchema # a circular import

class SocialAccountSchema(BaseModel):
    provider: str
    provider_user_id: str
    user_id: UUID4
    email_id: UUID4

    @classmethod
    def convert_data(cls, google_user: GoogleUserInfo, user, email) -> "SocialAccountSchema":
        return cls(
            provider="google",
            provider_user_id=google_user.id,
            user_id=user.id,
            email_id=email.id
        )
