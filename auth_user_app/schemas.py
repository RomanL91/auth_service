from typing import Annotated
from annotated_types import MinLen, MaxLen
from pydantic import BaseModel, EmailStr, ConfigDict, HttpUrl


# ====================================================
# Представлены базовые схемы для управления.
# Для наглядности они унаследованы от BaseModel
# и очень сильно похожи друг на друга, отличаясь
# практически только именем класса.
# ====================================================


class CreateUserSchema(BaseModel):
    username: Annotated[str, MinLen(3), MaxLen(20)]
    password: Annotated[str, MinLen(4), MaxLen(20)]
    email: EmailStr
    external_id: str | None = None


class ReadUserSchema(BaseModel):
    model_config = ConfigDict(strict=True)

    id: int
    username: str
    email: EmailStr | None = None


class UpdateUserSchema(BaseModel):
    model_config = ConfigDict(strict=True)

    username: str
    password: str

    email: EmailStr | None = None
    active: bool = True


class UpdateUserPartialSchema(BaseModel):
    model_config = ConfigDict(strict=True)

    username: str | None = None
    password: str | None = None

    email: EmailStr | None = None
    active: bool | None = None


class MSGUserErrorSchema(BaseModel):
    status_code: int
    message: str


class JWT(BaseModel):
    token_type: str
    access_token: str
    refresh_token: str | None = None


class RefreshRequestJWT(BaseModel):
    refresh_token: str


class GoogleUserInfo(BaseModel):
    id: str
    email: EmailStr
    verified_email: bool
    name: str
    given_name: str
    family_name: str
    picture: HttpUrl
