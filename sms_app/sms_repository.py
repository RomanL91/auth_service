from core.BASE_repository import SQLAlchemyRepository

from sms_app.models import SMSCode


class SMSCodeRepository(SQLAlchemyRepository):
    model = SMSCode
