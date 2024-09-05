from user_app.models import UserT
from core.BASE_repository import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):
    model = UserT
