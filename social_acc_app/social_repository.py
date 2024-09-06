from social_acc_app.models import SocialAccount
from core.BASE_repository import SQLAlchemyRepository


class SocialAccountRepository(SQLAlchemyRepository):
    model = SocialAccount
