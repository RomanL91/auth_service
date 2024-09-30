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
            select(UserT)
            .distinct(UserT.id)
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

    async def get_user_details(self, user_id: str):
        try:
            stmt = (
                select(UserT)
                .where(UserT.id == user_id)
                .options(
                    selectinload(UserT.emails),
                    selectinload(UserT.social_accounts),
                    selectinload(UserT.phone_number),
                )
            )

            # Выполняем запрос и получаем результат
            result = await self.session.execute(stmt)
            user = result.scalar_one_or_none()

            if user is None:
                raise ValueError("Пользователь не найден")

            # Форматируем результат в словарь или другую структуру
            # у меня есть UserDetailSchema и по сути результат запроса в БД
            # можно сразу преобразовывать и валидировать в эту модель, но я
            # решил делать это уровнем позже, а тут возвращать словарь
            user_data = {
                "user": {
                    "id": user.id,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "last_login": user.last_login,
                    "active": user.active,
                    "external_id": user.external_id,
                    "client_uuid": user.client_uuid,
                },
                "emails": [
                    {"id": email.id, "email": email.email} for email in user.emails
                ],
                "social_accounts": [
                    {
                        "id": sa.id,
                        "provider": sa.provider,
                        "provider_user_id": sa.provider_user_id,
                    }
                    for sa in user.social_accounts
                ],
                "phone_number": {
                    "id": user.phone_number.id if user.phone_number else None,
                    "phone_number": (
                        user.phone_number.phone_number if user.phone_number else None
                    ),
                },
            }

            return user_data

        except Exception as e:
            print(f"Ошибка при получении информации о пользователе: {e}")
            return None
