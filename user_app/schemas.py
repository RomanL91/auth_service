from uuid import uuid4
from typing import Annotated
from pydantic import BaseModel, ConfigDict, Field, UUID4


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
        ),
    ] = uuid4()
    first_name: Annotated[
        str | None,
        Field(..., description="Имя пользователя."),
    ] = None
    last_name: Annotated[
        str | None,
        Field(..., description="Фамилия пользователя."),
    ] = None
    active: Annotated[
        bool | None,
        Field(
            ...,
            description="Статус активности пользователя.",
        ),
    ] = True
