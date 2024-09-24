from core.BASE_unit_of_work import IUnitOfWork


class SMSService:

    async def create_sms_code(self, uow: IUnitOfWork, data):
        async with uow:
            sms_code = await uow.sms.create_obj(data)
            await uow.commit()
            return sms_code
