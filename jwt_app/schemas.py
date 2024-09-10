from datetime import datetime
from pydantic import BaseModel, UUID4


class JWTokenSchema(BaseModel):
    user_id: UUID4
    issued_at: datetime
    expires_at: datetime
    token_type: str
    token: str
    revoked: bool = False


class JWT(BaseModel):
    token: str


class JWTokensCreate(BaseModel):
    access: JWTokenSchema
    refresh: JWTokenSchema


class JWTokensResponse(BaseModel):
    access: JWT
    refresh: JWT
