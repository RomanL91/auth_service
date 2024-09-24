from abc import ABC, abstractmethod

from core.BASE_unit_of_work import IUnitOfWork
from core.function_utils import generate_six_digit_code

from sms_app.schemas import SMSCodeSchema
from phone_num_app.schemas import PhoneNumberSchemaResponse


class AuthStrategy(ABC):
    @abstractmethod
    async def authenticate(
        self,
        uow: IUnitOfWork,
        user_data: dict,
    ) -> SMSCodeSchema:
        pass


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
        return phone_data.phone_number, sms_code


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
        return phone.phone_number, sms_code


class AuthContext:
    def __init__(self, strategy: AuthStrategy):
        self.strategy = strategy

    async def execute(self, uow: IUnitOfWork, data: dict) -> SMSCodeSchema:
        return await self.strategy.authenticate(uow, data)
