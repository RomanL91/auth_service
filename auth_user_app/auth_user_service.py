from core.BASE_unit_of_work import IUnitOfWork
from auth_user_app.models import User
from auth_user_app.schemas import (
    CreateUserSchema,
    ReadUserSchema,
    UpdateUserSchema,
    UpdateUserPartialSchema,
)


class UserService:
    async def create_user(self, uow: IUnitOfWork, new_user: CreateUserSchema) -> User:
        user_dict = new_user.model_dump()
        async with uow:
            user = await uow.user.create_obj(user_dict)
            await uow.commit()
            return user

    async def get_users(self, uow: IUnitOfWork) -> list[User]:
        async with uow:
            return await uow.user.get_all_objs()

    async def get_user_by_id(self, uow: IUnitOfWork, user_id: int) -> User:
        async with uow:
            return await uow.user.get_obj(id=user_id)

    async def update_user(
        self,
        uow: IUnitOfWork,
        user_id: int,
        user_update: UpdateUserSchema | UpdateUserPartialSchema,
        partial: bool = False,
    ) -> User:
        data = user_update.model_dump(exclude_unset=partial)
        async with uow:
            user = await uow.user.update_obj(obj_id=user_id, data=data)
            await uow.commit()
            return user

    async def delete_user(self, uow: IUnitOfWork, user_id: int) -> None:
        async with uow:
            await uow.user.delete_obj(obj_id=user_id)
            await uow.commit()
