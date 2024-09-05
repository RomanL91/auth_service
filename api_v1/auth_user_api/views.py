from typing import Annotated

from fastapi import APIRouter, Response, Depends, HTTPException, Form, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from auth_user_app import schemas
from auth_user_app.auth_user_service import UserService

from api_v1.auth_user_api.dependencies import UOF_Depends


router = APIRouter(tags=["Users"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token/")


@router.post(
    "/",
    response_model=schemas.ReadUserSchema | schemas.MSGUserErrorSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    new_user: schemas.CreateUserSchema, uow: UOF_Depends, response: Response
):
    try:
        return await UserService().create_user(uow=uow, new_user=new_user)
    except HTTPException as error:
        response.status_code = error.status_code
        response_msg = schemas.MSGUserErrorSchema(
            status_code=error.status_code, message=error.detail
        )
        return response_msg


@router.get("/", response_model=list[schemas.ReadUserSchema])
async def get_users(uow: UOF_Depends):
    return await UserService().get_users(uow)


@router.get("/{user_id}/", response_model=schemas.ReadUserSchema)
async def get_user_by_id(user_id: int, uow: UOF_Depends):
    return await UserService().get_user_by_id(uow=uow, user_id=user_id)


@router.put("/{user_id}/", response_model=schemas.ReadUserSchema)
async def update_user(
    uow: UOF_Depends,
    user_id: int,
    user_update: schemas.UpdateUserSchema,
):
    return await UserService().update_user(
        uow=uow, user_id=user_id, user_update=user_update
    )


@router.patch("/{user_id}/", response_model=schemas.ReadUserSchema)
async def update_user(
    uow: UOF_Depends,
    user_id: int,
    user_update: schemas.UpdateUserPartialSchema,
):
    return await UserService().update_user(
        uow=uow, user_id=user_id, user_update=user_update, partial=True
    )


@router.delete("/{user_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(uow: UOF_Depends, user_id: int) -> None:
    await UserService().delete_user(uow=uow, user_id=user_id)


# @router.post("/login/", response_model=schemas.JWT)
# async def issue_jwt(uow: UOF_Depends, user_name: str = Form(), password: str = Form()):
#     jwt = await UserService().validate_user(
#         uow=uow, user_name=user_name, password=password
#     )
#     return jwt


@router.post("/token/", response_model=schemas.JWT)
async def issue_jwt(
    uow: UOF_Depends,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    jwt = await UserService().validate_user(
        uow=uow, user_name=form_data.username, password=form_data.password
    )
    return jwt


from auth_user_app.auth_user_service import jwt_service


# TODO можно вынести эту логику в UserService по подобию issue_jwt
@router.post("/refresh/", response_model=schemas.JWT, response_model_exclude_none=True)
async def refresh_jwt(refresh_token: schemas.RefreshRequestJWT):
    payload = jwt_service.decode_jwt(refresh_token.refresh_token)
    token_type = payload.get(jwt_service.token_type_field, "")
    if token_type != jwt_service.refresh_token_type:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid JWT token",
        )
    user_id = payload.get("user_id", 0)
    access_token = jwt_service.encode_jwt(
        payload={
            "user_id": user_id,
            jwt_service.token_type_field: jwt_service.access_token_type,
        }
    )
    return schemas.JWT(
        token_type=jwt_service.token_type,
        access_token=access_token,
        # refresh_token=refresh_token
    )


import requests
from core.settings import settings


@router.get("/login/google/")
async def login_google():
    return {
        "url": f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={settings.google_auth.google_client_id}&redirect_uri={settings.google_auth.google_redirect_url}&scope=openid%20profile%20email&access_type=offline"
    }


@router.get("/auth/google", response_model=schemas.JWT)
async def auth_google(uow: UOF_Depends, code: str):
    # TODO убрать http requests из view в отдельный сервис
    response = requests.post(
        settings.google_auth.google_token_url,
        data=settings.google_auth.get_data_to_post(code),
    )
    access_token = response.json().get("access_token")
    user_info = requests.get(
        settings.google_auth.google_user_info_url,
        headers=settings.google_auth.get_headers(access_token),
    )
    print(f"--- user_info --- >>> {user_info.json()}")
    # TODO 2 функции в одной, декомпозировать
    jwt = await UserService().get_or_create_user_and_generate_tokens(
        uow=uow, user_data=user_info.json(), external_id_use=True
    )

    return jwt
