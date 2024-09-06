import httpx

# == Core
from core import settings
from core.BASE_unit_of_work import IUnitOfWork

# == Exceptions
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError, NoResultFound

# == Schemas
from user_app.schemas import User, SaveUserSchema
from social_acc_app.schemas import CodeFromGoogle, GoogleUserInfo


class UserService:
    async def create_user(self, uow: IUnitOfWork, new_user: User) -> SaveUserSchema | None:
        user_dict = User.from_google_info(new_user).model_dump()
        async with uow:
            try:
                user = await uow.user.create_obj(user_dict)
                await uow.commit()
                return user
            except IntegrityError as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=e,  # TODO пока что показываем ошибки
                )

    async def get_user_info_from_google(
        self, code: CodeFromGoogle
    ) -> GoogleUserInfo | None:
        async with httpx.AsyncClient() as client:
            token_response = await client.post(
                settings.google_auth.google_token_url,
                data=settings.google_auth.get_data_to_post(code.code),
            )
            token_data = token_response.json()
            access_token = token_data.get("access_token", False)

            # Если токен получен успешно
            if access_token:
                # Получаем информацию о пользователе с помощью access_token
                user_info_response = await client.get(
                    settings.google_auth.google_user_info_url,
                    headers=settings.google_auth.get_headers(access_token),
                )
                user_info = GoogleUserInfo(**user_info_response.json())
                return user_info
            else:
                return None
