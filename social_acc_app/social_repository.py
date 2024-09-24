from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from social_acc_app.models import SocialAccount
from core.BASE_repository import SQLAlchemyRepository


class SocialAccountRepository(SQLAlchemyRepository):
    model = SocialAccount

    async def get_social_acc_by_provider_and_user_id(
        self, provider: str = None, user_id: str = None
    ):
        stmt = (
            select(self.model)
            .options(selectinload(self.model.user))
            .filter(
                self.model.provider == provider,
                self.model.user_id == user_id,
            )
        )
        result = await self.session.execute(stmt)
        social_acc = result.scalar_one_or_none()
        return social_acc
