from auth_user_app.models import User
from core.BASE_repository import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):
    model = User
