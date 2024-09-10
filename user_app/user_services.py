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
from jwt_app.schemas import JWTokensResponse

from email_app.email_services import EmailService
from social_acc_app.social_services import SocialService
from jwt_app.jwt_services import JWTService


class UserService:
    async def create_user(
        self, uow: IUnitOfWork, new_user: User
    ) -> SaveUserSchema | None:
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

    async def get_user_by_email(self, uow: IUnitOfWork, email: str) -> User:
        async with uow:
            return await uow.user.get_user_by_email(email)

    async def auth_google(self, uow: IUnitOfWork, data: CodeFromGoogle) -> JWTokensResponse:
        # может это паттерн цепочка обязанностей?
        data_user_google = await UserService().get_user_info_from_google(data)
        user = await self.get_user_by_email(uow=uow, email=data_user_google.email)
        if user is not None:
            jwt = await JWTService().create_jwt(
                uow=uow,
                user=user,
            )
            return jwt
        user = await UserService().create_user(
            uow=uow, new_user=data_user_google
        )
        email = await EmailService().create_email(
            uow=uow,
            google_user=data_user_google,
            user=user,
        )
        social = await SocialService().create_social_acc(
            uow=uow,
            google_user=data_user_google,
            user=user,
            email=email,
        )
        jwt = await JWTService().create_jwt(
            uow=uow,
            user=user,
        )
        return jwt
