from core.BASE_unit_of_work import IUnitOfWork
from auth_user_app.models import User
from auth_user_app.schemas import (
    CreateUserSchema,
    ReadUserSchema,
    UpdateUserSchema,
    UpdateUserPartialSchema,
    JWT,
)
from core import settings

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
        token = jwt_service.encode_jwt(payload={"user_id": user.id})
        return JWT(token_type="Bearer", access_token=token)


class JWTService:
    def __init__(
        self, private_key: str, public_key: str, algorithm: str, token_expire: int
    ):
        self.private_key = private_key
        self.public_key = public_key
        self.algorithm = algorithm
        self.token_expire = token_expire

    def encode_jwt(self, payload: dict, algorithm: str = None) -> str:
        algorithm = algorithm or self.algorithm
        # TODO работа со временем
        now = datetime.now(settings.auth_jwt.timezone) 
        expire = now + timedelta(minutes=self.token_expire)
        payload.update(exp=expire, iat=now)
        return jwt.encode(payload=payload, key=self.private_key, algorithm=algorithm)

    def decode_jwt(self, jwt_key: str | bytes, algorithm: str = None) -> dict:
        algorithm = algorithm or self.algorithm
        return jwt.decode(jwt=jwt_key, key=self.public_key, algorithms=[algorithm])


jwt_service = JWTService(
    private_key=settings.auth_jwt.private_key_path.read_text(),
    public_key=settings.auth_jwt.public_key_path.read_text(),
    algorithm=settings.auth_jwt.algoritm,
    token_expire=settings.auth_jwt.access_token_expire,
)
