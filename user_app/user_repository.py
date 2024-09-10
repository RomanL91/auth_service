from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from user_app.models import UserT
from email_app.models import Email
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
