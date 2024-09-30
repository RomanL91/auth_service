from fastapi import APIRouter, Response, status

# === Services
from sms_app.sms_service import SMSService
from phone_num_app.phone_services import PhoneService

from api_v1.api_dependencies import UOF_Depends, SMSCode_Depends

# === Schemas
from jwt_app.schemas import JWTokensResponse
from phone_num_app.schemas import PhoneNumberSchema, PhoneNumberSchemaResponse


router = APIRouter(tags=["phone"])


@router.post(
    "/login/phone",
    status_code=status.HTTP_200_OK,
    response_model=PhoneNumberSchemaResponse,
    summary="Получить ID записи телефонного номера.",
    description="""
        Через данный endpoint будет создана новая запись в БД или
        получена существующая о телефонном номере. 
        Возращает ID записи.
    """,
)
async def login_phone(
    uow: UOF_Depends, phone_num_schema: PhoneNumberSchema
) -> PhoneNumberSchemaResponse:
    phone_id = await PhoneService().login_phone(
        uow=uow, data_request_body=phone_num_schema
    )
    return phone_id


@router.get(
    "/auth/phone",
    status_code=status.HTTP_201_CREATED,
    response_model=JWTokensResponse | None,
    summary="Получить JWT.",
    description="""
        Через данный endpoint будут выданы ключи доступа.
        Требуется СМС код, который не был использован.
        Требуется ID записи телефонного номера.
        Валидация query прописана.
        Если данные валидны и АКТУАЛЬНЫ - вернет ключи со статусом 201.
        Если же данные валидны, НО НЕ АКТУЛЬНЫ - вернете ничего со статусом 204.
    """,
    responses={
        204: {
            "description": "code или phone_number_id не актуальны или не были найдены.",
            "content": {"application/json": {"example": None}},
        }
    },
)
async def auth_phone(
    uow: UOF_Depends, sms_code_form: SMSCode_Depends, response: Response
):
    code = await SMSService().chec_sms_code(
        uow=uow,
        code=sms_code_form.code,
        phone_number_id=sms_code_form.phone_number_id,
    )
    # немного логики в представлении
    if code:
        return await SMSService().mark_code_as_used_and_issued_tokens(
            uow=uow,
            sms_code_id=code.id,
        )
    response.status_code = status.HTTP_204_NO_CONTENT
    return None
