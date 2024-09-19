from abc import ABC, abstractmethod

from core.BASE_unit_of_work import IUnitOfWork

from jwt_app.schemas import JWTokensResponse


class AuthStrategy(ABC):
    @abstractmethod
    async def authenticate(
        self, 
        uow: IUnitOfWork, 
        user_data: dict,
    ) -> JWTokensResponse:
        pass


class ExistingUserStrategy(AuthStrategy):
    def __init__(
            self, 
            social_service, 
            jwt_service,
        ):
        self.social_service = social_service
        self.jwt_service = jwt_service
    
    async def authenticate(self, uow: IUnitOfWork, user_data: dict) -> JWTokensResponse:
        user = user_data['user'] # from DB
        # data_user = user_data['data_user'] # from SocAcc
        customized_user_data = user_data['customized_user_data']

        # Проверка, существует ли социальный аккаунт
        social_account = await self.social_service.get_social_acc_by_provider_and_user_id(
                uow=uow,
                provider=customized_user_data.provider,
                user_id=user.id,
            )
        if social_account is None:
            # Если социального аккаунта нет, создаем его для существующего пользователя
            await self.social_service.create_social_acc(
                uow=uow,
                data_user=customized_user_data,
                user_id=user.id,
                email_id=user.emails[0].id  # Предполагается, что email уже существует
            )

        # Создаем JWT для существующего пользователя
        jwt = await self.jwt_service.create_jwt(uow=uow, user=user)
        return jwt
    

class NewUserStrategy(AuthStrategy):
    def __init__(
            self, 
            social_service, 
            jwt_service,
            user_service,
            email_service,
        ):
        self.social_service = social_service
        self.jwt_service = jwt_service
        self.user_service = user_service
        self.email_service = email_service
    
    async def authenticate(self, uow: IUnitOfWork, user_data: dict) -> JWTokensResponse:
        customized_user_data = user_data['customized_user_data']

        # Создаем нового пользователя
        user = await self.user_service.create_user(uow=uow, new_user=customized_user_data)

        # Создаем email
        email = await self.email_service.create_email(
            uow=uow,
            data_user=customized_user_data,
            user_id=user.id
        )

        # Создаем социальный аккаунт
        await self.social_service.create_social_acc(
            uow=uow,
            data_user=customized_user_data,
            user_id=user.id,
            email_id=email.id
        )

        # Создаем JWT для нового пользователя
        jwt = await self.jwt_service.create_jwt(uow=uow, user=user)
        return jwt
    

class AuthContext:
    def __init__(self, strategy: AuthStrategy):
        self.strategy = strategy

    async def execute(self, uow: IUnitOfWork, user_data: dict) -> JWTokensResponse:
        return await self.strategy.authenticate(uow, user_data)