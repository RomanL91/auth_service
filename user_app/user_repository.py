from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from user_app.models import UserT
from email_app.models import Email
from social_acc_app.models import SocialAccount
from core.BASE_repository import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):
    model = UserT

    async def get_user_by_email(self, email: str):
        stmt = (
            select(UserT)
            .join(Email)
            .filter(Email.email == email)
            .options(selectinload(UserT.emails))  # Загрузка связанных email записей
        )
        result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()  # Возвращает одного пользователя или None
        return user

    async def get_user_by_social_id(self, social_id: str):
        stmt = (
            select(UserT)
            .join(SocialAccount)
            .filter(SocialAccount.provider_user_id == social_id)
            .options(
                selectinload(UserT.social_accounts)
            )  # Загрузка связанных social_accounts записей
        )
        result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()  # Возвращает одного пользователя или None
        return user

    async def get_user_by_social_or_email(
        self, email: str = None, provider_user_id: str = None
    ):
        # Строим запрос к таблице пользователей с объединением email и social_accounts
        stmt = (
            select(UserT).distinct(UserT.id)
            .join(Email)  # Соединяем таблицу email
            .join(SocialAccount)  # Соединяем таблицу социальных аккаунтов
            .filter(
                (Email.email == email)
                | (SocialAccount.provider_user_id == provider_user_id)
            )  # Применяем фильтры
            .options(
                selectinload(UserT.emails), selectinload(UserT.social_accounts)
            )  # Загружаем связанные сущности
        )
        # Выполняем запрос
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
