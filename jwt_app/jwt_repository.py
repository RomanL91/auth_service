from jwt_app.models import JWToken
from core.BASE_repository import SQLAlchemyRepository


class JWTRepository(SQLAlchemyRepository):
    model = JWToken
