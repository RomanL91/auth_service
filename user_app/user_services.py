import httpx

# == Core
from core import settings
from core.BASE_unit_of_work import IUnitOfWork

# == Exceptions
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

# == Schemas
from user_app.schemas import User
from social_acc_app.schemas import GoogleForm, VKForm, DataUserForMyService
from jwt_app.schemas import JWTokensResponse

# == Services
from jwt_app.jwt_services import JWTService
from email_app.email_services import EmailService
from social_acc_app.social_services import SocialService

from user_app.adapter import UserFactoryAdapter


class UserService:
    # TODO Внедрение Unit of Work на уровне сервиса
    # def __init__(self, uow: IUnitOfWork):
        # self.uow = uow
    # Вместо того чтобы передавать uow в каждый метод, можно внедрить uow в сам сервис, 
    # а управление транзакциями осуществлять на уровне класса сервиса. 
    # Это уменьшит количество передаваемых параметров
    
    exclude = ("email", "ava", "provider_user_id", "provider")

    async def get_user_by_socia_id(self, uow: IUnitOfWork, social_id: str) -> User:
        async with uow:
            return await uow.user.get_user_by_social_id(social_id)
        
    async def get_user_by_social_or_email(self, uow: IUnitOfWork, email: str = None, provider_user_id: str = None):
        async with uow:
            return await uow.user.get_user_by_social_or_email(email, provider_user_id)

    async def create_user(
        self, uow: IUnitOfWork, new_user: DataUserForMyService
    ) -> User | None:
        user_dict = new_user.model_dump(
            exclude=self.exclude
        )
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

    async def auth_google(self, uow: IUnitOfWork, data_google_form: GoogleForm) -> JWTokensResponse:
        data_form_google = data_google_form.model_dump()
        settings.google_auth.data_post = data_form_google
        access_token_google = await self.get_access_key_from_oauth_service(
            url=settings.google_auth.google_token_url,
            payload_template=settings.google_auth.data_post,
        )
        # получение инфы о пользователе
        data_user_from_google = await UserFactoryAdapter.fetch_user_info(
            url=settings.google_auth.google_user_info_url,
            headers=settings.google_auth.get_headers(access_token_google)
        )
        # адаптирую для БД сервиса
        customized_user_data = UserFactoryAdapter.create_user(
            data=data_user_from_google, source="google"
        )
        # проверка на существование
        user = await self.get_user_by_social_or_email(
            uow=uow,
            email=data_user_from_google.email,
            provider_user_id=data_user_from_google.id
        )
        if user is not None:
            jwt = await JWTService().create_jwt(
                uow=uow,
                user=user,
            )
            return jwt
        user = await self.create_user(
            uow=uow, new_user=customized_user_data
        )
        email = await EmailService().create_email(
            uow=uow,
            data_user=customized_user_data,
            user_id=user.id,
        )
        social = await SocialService().create_social_acc(
            uow=uow,
            data_user=customized_user_data,
            user_id=user.id,
            email_id=email.id,
        )
        jwt = await JWTService().create_jwt(
            uow=uow,
            user=user,
        )
        return jwt

    async def auth_vk(self, uow: IUnitOfWork, params: VKForm) -> JWTokensResponse:
        data_form_vk = params.model_dump()
        settings.vk_auth.data_post_request_to_receive_keys = data_form_vk
        test_access_vk = await self.get_access_key_from_oauth_service(
            url=settings.vk_auth.vk_token_url,
            headers=settings.vk_auth.headers,
            payload_template=settings.vk_auth.data_post_request_to_receive_keys,
        )
        # получение инфы о пользователе
        test_data_user = await UserFactoryAdapter.fetch_user_info(
            url=settings.vk_auth.vk_user_info_url,
            data=settings.vk_auth.get_data_payload(test_access_vk),
            request_method="POST",
        )
        # адаптирую для БД сервиса
        customized_user_data = UserFactoryAdapter.create_user(
            data=test_data_user, source="vk"
        )
        # проверка на существование
        user = await self.get_user_by_social_or_email(
            uow=uow,
            email=test_data_user.email,
            provider_user_id=test_data_user.user_id
        )
        if user is not None:
            jwt = await JWTService().create_jwt(
                uow=uow,
                user=user,
            )
            return jwt
        user = await self.create_user(
            uow=uow, new_user=customized_user_data
        )
        email = await EmailService().create_email(
            uow=uow,
            data_user=customized_user_data,
            user_id=user.id,
        )
        social = await SocialService().create_social_acc(
            uow=uow,
            data_user=customized_user_data,
            user_id=user.id,
            email_id=email.id,
        )
        jwt = await JWTService().create_jwt(
            uow=uow,
            user=user,
        )
        return jwt


    async def get_access_key_from_oauth_service(
        self,
        url: str,
        payload_template: dict,
        headers: dict = {},
    ):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url=url,
                headers=headers,
                data=payload_template,
            )
            response_data = response.json()
            access_token = response_data.get("access_token", False)
            
            if access_token:
                return access_token
