from datetime import datetime
from pydantic import BaseModel, ConfigDict, UUID4, Field


class JWTokenSchema(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        strict=True,
        json_schema_extra={
            "example": {
                "user_id": "2cdb7fba2050471792632ebe72bf0267",
                "issued_at": "2024-09-27T23:39:31.781647+05:00",
                "expires_at": "2024-09-27T23:44:31.781647+05:00",
                "token_type": "access_token",
                "token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMmNkYjdmYmEtMjA1MC00NzE3LTkyNjMtMmViZTcyYmYwMjY3IiwidHlwZSI6ImFjY2Vzc190b2tlbiIsImV4cCI6MTcyNzQ2MjY3MSwiaWF0IjoxNzI3NDYyMzcxfQ.BZ-NLCWzuwGtqEFsf6Nshex7ag5SCqOODg7D909RerCI91wjkTkklPii0DP1A98ydabMe6F3hBmP65umCFTDeGMt1Oi1ohBk3O8rHBoEdomseg4HepjnAKzpPWa-9GHeleFlVKOwYevYjw86mGJg5-evT8XAdHVv3MkX4Wwg74mUecUiAc_DOktb73cHWf4nh6j2LbdTcyIgh2pSQasopT6z2hV6oKRwn3lqX7ECADG6lDVZ66DnD0xXPmgDr7xXVt4X8vi1OsspYIQhoeKLUvkpqOGsI4Q6KGX71geqAkEWVb7G2NdkmUbWdBvfbfQo7caOIR8S8hsin6BS52E6DQ",
                "revoked": False,
            }
        },
    )
    user_id: UUID4
    issued_at: datetime
    expires_at: datetime
    token_type: str
    token: str
    revoked: bool = False


class JWT(BaseModel):
    # token: str
    token: str = Field(
        ...,
        description="JWT токен",
        example="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNDNiYjNkOTQtNGZjOC00MjYzLTg5OTItZjk4ZDNhODU5NDM0IiwidHlwZSI6ImFjY2Vzc190b2tlbiIsImV4cCI6MTcyNzQxNjk2OCwiaWF0IjoxNzI3NDE2NjY4fQ.go4FmVy1ysV4Xxe7ysTrFIjZf2tujantBWE-uP7amHgcQWv8pYR-rDYCB_EnDpQMJtRes-QjsNTDA430mBbM6kjMM-UcbYti89iT9ZQnUZGuuwSoVbTw-lwjquzcCz9cuXWOzdNynk-Gtbdjh2--rWYE2NC5U3R5LJWL2OaoIbWSMYqMJn8PVgzhSSqJfKNhczjdzVF5v5HK8lfZBg2Dj9nSMULOGeplbWeHcyoAPmLkDqiF-6cRii-zplTtL89fajBd4ldDJiZPtQ3LCASHpiMgNjdQN5E7oZ4NdtRzXIFXskKLpc7bsWElR_XKBhYpqtyrs41PpdUxFdxSLGVHkQ",
    )


class JWTokensCreate(BaseModel):
    access: JWTokenSchema
    refresh: JWTokenSchema


class JWTokensResponse(BaseModel):
    access: JWT
    refresh: JWT
