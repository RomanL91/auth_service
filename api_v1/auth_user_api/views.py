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
