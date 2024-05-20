from fastapi import APIRouter, status

from auth_user_app import schemas
from auth_user_app.auth_user_service import UserService

from api_v1.auth_user_api.dependencies import UOF_Depends


router = APIRouter(tags=["Users"])


@router.post(
    "/", response_model=schemas.ReadUserSchema, status_code=status.HTTP_201_CREATED
)
async def create_user(new_user: schemas.CreateUserSchema, uow: UOF_Depends):
    return await UserService().create_user(uow=uow, new_user=new_user)


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
