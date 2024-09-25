import re
from typing import Annotated
from pydantic import BaseModel, Field, ConfigDict, UUID4


# Валидация номера телефона
def validate_phone_number(value: str) -> str:
    if not re.match(r"^\d{7,15}$", value):
        raise ValueError(
            "Номер телефона должен содержать только цифры и быть длиной от 7 до 15 символов."
        )
    return value


class PhoneNumberSchemaResponse(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        strict=True,
        json_schema_extra={
            "example": {
                "id": "2cdb7fba2050471792632ebe72bf0267",
            }
        },
    )
    id: UUID4


# Pydantic модель для телефонных номеров
class PhoneNumberSchema(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        strict=True,
        json_schema_extra={
            "example": {
                "country_code": "+7",
                "number": "1234567890",
            }
        },
    )
    country_code: Annotated[
        str,
        Field(
            ...,
            pattern=r"^\+\d{1,3}$",  # Используем pattern вместо regex
            description="Код страны, начиная с '+'. Пример: +1, +44, +7",
        ),
    ]
    number: Annotated[
        str,
        Field(
            ...,
            description="Основной номер телефона, без пробелов и дефисов. Пример: 1234567890",
        ),
    ]

    formatted_number: str = Field(
        None, description="Отформатированный номер телефона, например +1 123-456-7890"
    )

    def model_post_init(self, __context):
        # Автоматическое формирование formatted_number после инициализации модели
        self.formatted_number = f"{self.country_code}-{self.number[:3]}-{self.number[3:6]}-{self.number[6:]}"
        # Валидация поля number
        self.number = validate_phone_number(self.number)
