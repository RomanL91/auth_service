from abc import ABC, abstractmethod

from smsc_api import SMSC
from core.BASE_unit_of_work import IUnitOfWork
from core.function_utils import generate_six_digit_code

from sms_app.schemas import SMSCodeSchema
from phone_num_app.schemas import PhoneNumberSchemaResponse


class AuthStrategy(ABC):
    sms = SMSC()

    @abstractmethod
    async def authenticate(
        self,
        uow: IUnitOfWork,
        user_data: dict,
    ) -> SMSCodeSchema:
        pass

    def send_sms(
        self,
        phone_number: str,
        code: str,
        sender: str = "sms",
    ):
        msg = f"Код авторизации: {code} SCK-1.KZ"  # TODO вынести в настройки
        phone_number = phone_number.replace("+", "").replace("-", "")
        self.sms.send_sms(
            phones=phone_number,
            message=msg,
            sender=sender,
        )


class ExistingPhoneStrategy(AuthStrategy):
    def __init__(self, phone_service, sms_service):
        self.phone_service = phone_service
        self.sms_service = sms_service

    async def authenticate(
        self,
        uow: IUnitOfWork,
        phone_data: PhoneNumberSchemaResponse,
    ) -> SMSCodeSchema:
        sms_code = generate_six_digit_code()
        data = {"phone_number_id": phone_data.id, "code": sms_code}
        sms = await self.sms_service().create_sms_code(
            uow=uow,
            data=data,
        )
        phone_num = phone_data.phone_number
        self.send_sms(phone_number=phone_data.phone_number, code=sms_code)
        return PhoneNumberSchemaResponse(id=phone_data.id)


class NewPhoneStrategy(AuthStrategy):
    def __init__(self, phone_service, sms_service):
        self.phone_service = phone_service
        self.sms_service = sms_service

    async def authenticate(
        self,
        uow: IUnitOfWork,
        phone_data: PhoneNumberSchemaResponse,
    ):
        sms_code = generate_six_digit_code()
        data = {"phone_number": phone_data.formatted_number}
        phone = await self.phone_service.create_phone(
            uow=uow,
            phone_number_data=data,
        )
        user = await self.phone_service.create_user_with_tel_number(
            uow=uow,
            first_name="No name",
            last_name="Anonim",
            phone_number_id=phone.id,
        )
        data = {"phone_number_id": phone.id, "code": sms_code}
        sms = await self.sms_service().create_sms_code(
            uow=uow,
            data=data,
        )
        self.send_sms(phone_number=phone_data.formatted_number, code=sms_code)
        return PhoneNumberSchemaResponse(id=phone.id)


class AuthContext:
    def __init__(self, strategy: AuthStrategy):
        self.strategy = strategy

    async def execute(self, uow: IUnitOfWork, data: dict) -> SMSCodeSchema:
        return await self.strategy.authenticate(uow, data)
