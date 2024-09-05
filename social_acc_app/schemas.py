from typing import Annotated
from annotated_types import MinLen, MaxLen
from pydantic import BaseModel, EmailStr, ConfigDict, HttpUrl


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
