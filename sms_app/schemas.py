from typing import Annotated
from pydantic import BaseModel, Field, ConfigDict, UUID4


# Pydantic модель для SMSCode
class SMSCodeSchema(BaseModel):
    model_config = ConfigDict(
        strict=True,
        populate_by_name=True,
        schema_extra={
            "example": {
                "code": "908-645",
                "is_used": False,
                "phone_number_id": "d7983b4c-6595-4c07-9d76-c8dbd80c8d8c",
            }
        },
    )
    code: Annotated[
        str,
        Field(
            ...,
            min_length=4,
            max_length=4,
            pattern=r"^\d{4}$",
            description="4-значный код в формате XXXX.",
        ),
    ]
    is_used: Annotated[
        bool,
        Field(default=False, description="Флаг, указывающий, был ли использован код."),
    ]
    phone_number_id: Annotated[
        UUID4, Field(..., description="ID телефонного номера, к которому привязан код.")
    ]


class SMSCOdeSchemaForm(BaseModel):
    model_config = ConfigDict(
        strict=True,
    )
    code: Annotated[
        str,
        Field(
            ...,
            min_length=4,
            max_length=4,
            pattern=r"^\d{4}$",
            description="4-значный код в формате XXXX.",
        ),
    ]
    phone_number_id: Annotated[
        UUID4,
        Field(
            ...,
            description="ID телефонного номера, к которому привязан код.",
        ),
    ]
