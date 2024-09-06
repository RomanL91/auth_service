from email_app.models import Email
from core.BASE_repository import SQLAlchemyRepository


class EmailRepository(SQLAlchemyRepository):
    model = Email
