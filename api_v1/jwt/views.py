from fastapi import APIRouter, status, HTTPException

# === Services
from jwt_app.jwt_services import JWTService, jwt_util

from api_v1.api_dependencies import UOF_Depends

# === Schemas
from jwt_app.schemas import JWT, JWTokenSchema


router = APIRouter(tags=["token"])


@router.post(
    "/refresh",
    status_code=status.HTTP_201_CREATED,
    response_model=JWTokenSchema,
    summary="Обновить ключ доступа.",
    description="""
        Через данный endpoint можно обновить ключ доступа типа access в обмен
        на ключ доступа типа refresh. 
    """,
    responses={
        400: {
            "description": "Получил это - высока вероятность, что отдаешь не тот тип ключа.",
            "content": {
                "application/json": {
                    "example": "Invalid token type"
                }
            },
        },
        401: {
            "description": "Это значит, что ключ 'битый' и не проходит проверку или же просто 'протух'.",
            "content": {
                "application/json": {
                    "example": "Invalid token type | Token expired"
                }
            },
        }
    }
)
async def refresh(uow: UOF_Depends, token: JWT):
    result_decode = jwt_util.decode_jwt(jwt_key=token.token)
    user_id = result_decode.get("user_id", None)
    token_type = result_decode.get("type", None)

    if token_type != jwt_util.refresh_token_type:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid token type",
        )
    
    access_token = await JWTService().generate_and_save_jwt(
        uow=uow, user_id=user_id, type=jwt_util.access_token_type)
    return access_token

