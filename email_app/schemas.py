from pydantic import BaseModel, ConfigDict, EmailStr, UUID4


class EmailSchema(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        strict=True,
        json_schema_extra={
            "example": {
                "user_id": "2cdb7fba2050471792632ebe72bf0267",
                "email": "user@example.com",
            }
        },
    )
    email: EmailStr
    user_id: UUID4


class EmailSchemaToUserDetail(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        strict=True,
        json_schema_extra={
            "example": {
                "id": "2cdb7fba2050471792632ebe72bf0267",
                "email": "user@example.com",
            }
        },
    )
    id: UUID4
    email: EmailStr
