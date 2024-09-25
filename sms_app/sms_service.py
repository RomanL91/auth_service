from core.BASE_unit_of_work import IUnitOfWork

from jwt_app.jwt_services import JWTService


class SMSService:

    async def create_sms_code(self, uow: IUnitOfWork, data):
        async with uow:
            sms_code = await uow.sms.create_obj(data)
            await uow.commit()
            return sms_code
        
    
    async def chec_sms_code(self, uow: IUnitOfWork, code: str, phone_number_id: str, is_used: bool = True,):
        async with uow:
            code = await uow.sms.get_obj(
                code=code,
                phone_number_id=phone_number_id,
                is_used=is_used,
            )
        return code
    

    async def mark_code_as_used_and_issued_tokens(self, uow: IUnitOfWork, sms_code_id: str,):
        async with uow:
            code = await uow.sms.update_obj(sms_code_id, {"is_used": False})
            user = await uow.user.get_obj(
                phone_number_id=code.phone_number_id,
            )
            jwt = await JWTService().create_jwt(
                uow=uow, user=user
            )
            await uow.commit()
            return jwt
