from uuid import uuid4
from typing import Annotated, List
from pydantic import BaseModel, ConfigDict, Field, UUID4, EmailStr

from email_app.schemas import EmailSchemaToUserDetail
from social_acc_app.schemas import SocialAccountSchemaToUserDetail
from phone_num_app.schemas import PhoneNumberSchemaToUserDetail
from jwt_app.schemas import JWT


class SaveUserSchema(BaseModel):
    model_config = ConfigDict(
        strict=True,
        from_attributes=True,
    )
    id: UUID4


class User(BaseModel):
    model_config = ConfigDict(
        strict=True,
    )
    id: Annotated[
        UUID4,
        Field(
            ...,
            description="Уникальный ID пользователя.",
            examples=["ea17b167-4c86-4998-856f-ba2ae775d953"],
        ),
    ] = uuid4()
    first_name: Annotated[
        str | None,
        Field(..., description="Имя пользователя.", examples=["Роман"]),
    ] = None
    last_name: Annotated[
        str | None,
        Field(..., description="Фамилия пользователя.", examples=["Лебедев"]),
    ] = None
    active: Annotated[
        bool | None,
        Field(
            ...,
            description="Статус активности пользователя.",
        ),
    ] = True


class UserDetailSchema(BaseModel):
    user: User
    emails: List[EmailSchemaToUserDetail]
    social_accounts: List[SocialAccountSchemaToUserDetail]
    phone_number: PhoneNumberSchemaToUserDetail


class UpdateUserSchema(BaseModel):
    token: JWT
    email: EmailStr | None = None
    phone_number: Annotated[
        str | None,
        Field(
            ..., 
            pattern=r"^(?:\+7|8)\d{10}$",
            description="Телефонный номер.", 
            examples=["+77714748717"],
        ),
    ] = None
    first_name: Annotated[
        str | None,
        Field(
            ..., 
            description="Имя пользователя.", 
            examples=["Роман"],
        ),
    ] = None
    last_name: Annotated[
        str | None,
        Field(
            ..., 
            description="Фамилия пользователя.", 
            examples=["Лебедев"],
        ),
    ] = None
