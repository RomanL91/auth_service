from uuid import uuid4
from typing import Annotated
from pydantic import BaseModel, ConfigDict, Field, UUID4

from social_acc_app.schemas import GoogleUserInfo


class SaveUserSchema(BaseModel):
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
        )
    ] = uuid4()
    firt_name: Annotated[str | None, Field(..., description="Имя пользователя.")] = None
    last_name: Annotated[
        str | None, Field(..., description="Фамилия пользователя.")
    ] = None
    # updated_at: Annotated[
    #     datetime | None,
    #     Field(
    #         ...,
    #         description="Время обновления пользователя в системе.",
    #     ),
    # ] = None
    # last_login: Annotated[
    #     datetime | None,
    #     Field(
    #         ...,
    #         description="Время последнего логина в системе.",
    #     ),
    # ] = None
    active: Annotated[
        bool | None,
        Field(
            ...,
            description="Статус активности пользователя.",
        ),
    ] = True
    # external_id: Annotated[
    #     int | str | None,
    #     Field(
    #         ...,
    #         description="Уникальный ID пользователя для интеграций с другими системами.",
    #     ),
    # ] = None
    # client_uuid: Annotated[
    #     UUID4,
    #     Field(
    #         ...,
    #         description="Уникальный ID с клиента",
    #     ),
    # ] = None
    # phone_number_id: Annotated[
    #     UUID4,
    #     Field(
    #         ...,
    #         description="Внешний ключ таблицы телефонных номеров.",
    #     ),
    # ] = None
    # phone_number: Optional[PhoneNumber] = None
    # emails: List[Email] = []
    # social_accounts: List[SocialAccount] = []
    # tokens: List[JWToken] = []

    @classmethod
    def from_google_info(cls, google_user: GoogleUserInfo) -> "User":
        return cls(
            firt_name=google_user.given_name,
            last_name=google_user.family_name,
        )
