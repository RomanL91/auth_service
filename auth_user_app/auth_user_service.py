from core.BASE_unit_of_work import IUnitOfWork
from auth_user_app.models import User
from auth_user_app.schemas import (
    CreateUserSchema,
    ReadUserSchema,
    UpdateUserSchema,
    UpdateUserPartialSchema,
    JWT,
)
from core.settings import SettingsAuth

# == Exceptions
from sqlalchemy.exc import IntegrityError, NoResultFound
from fastapi import HTTPException, status

# == bcrypt for hashed password
import bcrypt

# == jwt for create jwt-token
import jwt
from datetime import datetime, timedelta


class UserService:
    async def create_user(
        self, uow: IUnitOfWork, new_user: CreateUserSchema
    ) -> User | None:
        user_dict = new_user.model_dump()
        user_dict["password"] = self.password_hashed(user_dict["password"])
        async with uow:
            try:
                user = await uow.user.create_obj(user_dict)
                await uow.commit()
                return user
            except IntegrityError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Пользователь с таким именем уже существует.",
                )

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

    # TODO вынести логику хеширования
    def password_hashed(self, password: str) -> str:
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        return hashed_password.decode("utf-8")

    def check_password(self, password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))

    async def validate_user(
        self, uow: IUnitOfWork, user_name: str, password: str
    ) -> JWT | None:
        error_403 = HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Не верный логин или пароль.",
        )
        async with uow:
            try:
                user = await uow.user.get_obj(username=user_name)
            except NoResultFound:
                raise error_403
        if not self.check_password(password=password, hashed_password=user.password):
            raise error_403
        access_token = jwt_service.encode_jwt(
            payload={
                "user_id": user.id,
                jwt_service.token_type_field: jwt_service.access_token_type,
            }
        )
        refresh_token = jwt_service.encode_jwt(
            payload={
                "user_id": user.id,
                jwt_service.token_type_field: jwt_service.refresh_token_type,
            }
        )
        return JWT(
            token_type=jwt_service.token_type,
            access_token=access_token,
            refresh_token=refresh_token,
        )


class JWTService:
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

    def encode_jwt(self, payload: dict) -> str:
        now = datetime.now(self.timezone)
        expire = now + timedelta(minutes=self.access_token_expire)
        if self.refresh_token_type in payload.values():
            expire = now + timedelta(minutes=self.refresh_token_expire)
        payload.update(exp=expire, iat=now)
        return jwt.encode(
            payload=payload, key=self.private_key, algorithm=self.algorithm
        )

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


jwt_service = JWTService(settings=SettingsAuth())
