from core.BASE_repository import SQLAlchemyRepository

from phone_num_app.models import PhoneNumber


class PhoneRepository(SQLAlchemyRepository):
    model = PhoneNumber
