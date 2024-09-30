import uuid
import jwt
from datetime import datetime, timedelta

# == Core
from core.settings import SettingsAuth
from core.BASE_unit_of_work import IUnitOfWork

# == Exceptions
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

# == Schemas
from jwt_app.schemas import JWTokensCreate, JWTokenSchema
from user_app.schemas import SaveUserSchema


class JWTService:
    # TODO Нужен рефактор, повторы кода/функционала
    def generate_jwt(self, **payload):
        token = jwt_util.encode_jwt(payload)
        return token
    
    async def generate_and_save_jwt(self, uow: IUnitOfWork, **payload):
        token = self.generate_jwt(**payload)
        data_token = token.model_dump()
        async with uow:
            try:
                jwt_token = await uow.jwt.create_obj(data_token)
                await uow.commit()
                return token
            except IntegrityError as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=e,  # TODO показываем ошибки клиентской стороне для отладки, потом скрываем
                )

    def generate_access_and_refresh_jwt(
        self,
        user: SaveUserSchema,
    ) -> JWTokensCreate:
        user_id: str = str(user.id)
        access_token = jwt_util.encode_jwt(
            payload={
                "user_id": user_id,
                jwt_util.token_type_field: jwt_util.access_token_type,
            }
        )
        refresh_token = jwt_util.encode_jwt(
            payload={
                "user_id": user_id,
                jwt_util.token_type_field: jwt_util.refresh_token_type,
            }
        )
        tokens = JWTokensCreate(access=access_token, refresh=refresh_token)
        return tokens

    async def create_jwt(
        self,
        uow: IUnitOfWork,
        user: SaveUserSchema,
    ) -> JWTokensCreate:
        tokens: JWTokensCreate = self.generate_access_and_refresh_jwt(user)
        tokens_dict = tokens.model_dump()
        async with uow:
            try:
                for k, v in tokens_dict.items():
                    jwt_token = await uow.jwt.create_obj(v)
                await uow.commit()
                return tokens
            except IntegrityError as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=e,  # TODO показываем ошибки клиентской стороне для отладки, потом скрываем
                )


class JWTUtil:
    def __init__(self, settings: SettingsAuth):
        # super() ?? TODO
        self.private_key = settings.private_key_path.read_text()
        self.public_key = settings.public_key_path.read_text()
        self.algorithm = settings.algorithm
        self.access_token_expire = settings.access_token_expire
        self.refresh_token_expire = settings.refresh_token_expire
        self.timezone = settings.timezone
        self.token_type = settings.token_type
        self.token_type_field = settings.token_type_field
        self.access_token_type = settings.access_token_type
        self.refresh_token_type = settings.refresh_token_type

    def encode_jwt(self, payload: dict) -> JWTokenSchema:
        now = datetime.now(self.timezone)
        expire = now + timedelta(minutes=self.access_token_expire)
        if self.refresh_token_type in payload.values():
            expire = now + timedelta(minutes=self.refresh_token_expire)
        payload.update(exp=expire, iat=now)
        token_value = jwt.encode(
            payload=payload, key=self.private_key, algorithm=self.algorithm
        )
        token = JWTokenSchema(
            user_id=self.convet_str_to_uuid(payload.get("user_id")),
            issued_at=now,
            expires_at=expire,
            token_type=payload.get("type", "unknown"),
            token=token_value,
        )
        return token

    def decode_jwt(self, jwt_key: str) -> dict:
        # TODO Пересмотреть обработку исключений
        # return jwt.decode(jwt_key, key=self.public_key, algorithms=[self.algorithm])
        try:
            return jwt.decode(jwt_key, key=self.public_key, algorithms=[self.algorithm])
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired"
            )
        except jwt.InvalidTokenError as e:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
        except Exception as e:
            # Для любых других JWT ошибок
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid JWT token"
            )
        
    def convet_str_to_uuid(self, user_id: str):
        return uuid.UUID(user_id)


jwt_util = JWTUtil(settings=SettingsAuth())
