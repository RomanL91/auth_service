from fastapi import APIRouter, status, HTTPException

# === Services
from user_app.user_services import UserService
from jwt_app.jwt_services import jwt_util

from api_v1.api_dependencies import UOF_Depends

# === Schemas
from jwt_app.schemas import JWT
from user_app.schemas import UserDetailSchema, UpdateUserSchema


router = APIRouter(tags=["user"])


@router.post(
    "/info",
    status_code=status.HTTP_200_OK,
    response_model=UserDetailSchema,
    summary="Получить информацию о пользователе.",
    description="""
        Через данный endpoint можно получить информацию о пользователе
        в обмен на актуальный ключ доступа типа access. В противом
        случае, при подаче экспирированого ключа или 'сломанного' - 401
        код ошибки. В случае подачи ключа не правильного типа - 400 код. 
    """,
    responses={
        400: {
            "description": "Получил это - высока вероятность, что отдаешь не тот тип ключа.",
            "content": {"application/json": {"example": "Invalid token type"}},
        },
        401: {
            "description": "Это значит, что ключ 'битый' и не проходит проверку или же просто 'протух'.",
            "content": {
                "application/json": {"example": "Invalid token type | Token expired"}
            },
        },
    },
)
async def get_user_info(uow: UOF_Depends, token: JWT) -> UserDetailSchema:
    result_decode = jwt_util.decode_jwt(jwt_key=token.token)
    # если не выпали ошибки при decode_jwt достаем из результата ИД пользователя и тип токена
    user_id = result_decode.get("user_id", None)
    token_type = result_decode.get("type", None)
    # если тип токена не access, то и в БД не ходим
    if token_type != jwt_util.access_token_type:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid token type",
        )
    # запрос к БД о доступной информации о пользователе
    user_detail = await UserService().get_user_details(
        uow=uow,
        user_id=user_id,
    )
    return user_detail


@router.patch(
    "/pach",
)
async def user_patch(uow: UOF_Depends, update_data: UpdateUserSchema):
    result_decode = jwt_util.decode_jwt(jwt_key=update_data.token.token)
    # если не выпали ошибки при decode_jwt достаем из результата ИД пользователя и тип токена
    user_id = result_decode.get("user_id", None)
    token_type = result_decode.get("type", None)
    # если тип токена не access, то и в БД не ходим
    if token_type != jwt_util.access_token_type:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid token type",
        )
    return "бля забыл сделать"
    await UserService().update_user_info(uow=uow, update_data=update_data)
