from core.BASE_unit_of_work import IUnitOfWork

from sms_app.sms_service import SMSService

from phone_num_app import strategy as Strategy
from phone_num_app.schemas import PhoneNumberSchema, PhoneNumberSchemaResponse


class PhoneService:

    async def get_phone(self, uow: IUnitOfWork, **phone_number: str):
        async with uow:
            phone = await uow.phone.get_obj(**phone_number)
            return phone

    async def create_phone(
        self, uow: IUnitOfWork, phone_number_data: str
    ) -> PhoneNumberSchemaResponse:
        async with uow:
            phone = await uow.phone.create_obj(phone_number_data)
            await uow.commit()
            return phone

    async def create_user_with_tel_number(
        self, uow: IUnitOfWork, **phone_number_id: str
    ):
        async with uow:
            user = await uow.user.create_obj(phone_number_id)
            await uow.commit()
            return user

    async def login_phone(self, uow: IUnitOfWork, data_request_body: PhoneNumberSchema):
        phone = await self.get_phone(
            uow=uow, phone_number=data_request_body.formatted_number
        )
        # далее стратегия!
        if phone is None:
            # стратегия создания пользователя
            strategy = Strategy.NewPhoneStrategy(
                phone_service=self, sms_service=SMSService
            )
            context = data_request_body
        else:
            # стратегия к сущестующему пользователя
            strategy = Strategy.ExistingPhoneStrategy(
                phone_service=self, sms_service=SMSService
            )
            context = phone

        auth_context = Strategy.AuthContext(strategy=strategy)
        phone_id = await auth_context.execute(uow=uow, data=context)
        return phone_id
