from uuid import uuid4

from pydantic import BaseModel, EmailStr, HttpUrl, UUID4


class LinkToAuthenticationForm(BaseModel):
    url: HttpUrl


class ParametersOAuthForm(BaseModel):
    code: str


class GoogleForm(ParametersOAuthForm):
    pass


class VKForm(ParametersOAuthForm):
    device_id: str
    state: str


class DataUserForMyService(BaseModel):
    id: UUID4
    first_name: str
    last_name: str
    email: EmailStr
    provider: str
    provider_user_id: str
    ava: HttpUrl


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


class ParamsFormVK(BaseModel):
    code: str
    device_id: str
    state: str


class VKUserInfo(BaseModel):
    user_id: str
    first_name: str
    last_name: str
    email: EmailStr | str
    avatar: HttpUrl


class SocialAccountSchema(BaseModel):
    id: UUID4 = uuid4()
    provider: str
    provider_user_id: str
    user_id: UUID4
    email_id: UUID4
