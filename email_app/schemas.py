from pydantic import BaseModel, EmailStr, UUID4


class EmailSchema(BaseModel):
    email: EmailStr
    user_id: UUID4
