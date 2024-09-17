
from httpx import AsyncClient

from fastapi import APIRouter, status

# === Services
from user_app.user_services import UserService

# === Schemas
from jwt_app.schemas import JWTokensResponse
from social_acc_app.schemas import LinkToAuthenticationForm

from core.settings import settings
from core.function_utils import generate_code_verifier, generate_code_challenge

from api_v1.api_dependencies import UOF_Depends, ParamsVK_Depends


router = APIRouter(tags=["VK"])


@router.get(
    "/login/vk/",
    status_code=status.HTTP_200_OK,
    response_model=LinkToAuthenticationForm,
    summary="Получить ссылку, ведущию на форму авторизации VK.",
    description="""
        Через данный endpoint можно получить ссылку, 
        которая ведет на страницу с формой для авторизации через VK.
        Стоит учитывать, что данная ссылка не статична, её придется
        формировать для каждого пользователя. Из динамический элементов ссылки 
        можно выделить query параметры 'state' и 'code_challenge'.
    """,
)
async def login_vk():
    code_verifier = generate_code_verifier()
    code_challenge = generate_code_challenge(code_verifier)
    link_to_VK_authentication_form = settings.vk_auth.vk_base_url.format(
        state=code_verifier,
        code_challenge=code_challenge,
        vk_redirect_url=settings.vk_auth.vk_redirect_url,
    )

    async with AsyncClient() as client:
        response = await client.get(
            link_to_VK_authentication_form
        )
    if response.status_code == 302:
        redirect_url = response.headers.get('location')
        return {
            "url": redirect_url
        }
    return {f"No redirect, status code": {response.status_code}}


@router.get(
    "/auth/vk",
    status_code=status.HTTP_200_OK,
    response_model=JWTokensResponse,
    summary="Создаем Пользователя через учетку VK.",
    description="""
        Данный endpoint сохранен в настройках VK app и
        на него настроен редирект после того как пользователь 
        аутентифицируется на стороне VK. После чего будут полученны 
        данные профиля пользователя, сохранены в систему, созданы JWT.
    """,
)
async def auth_vk(uow: UOF_Depends, params: ParamsVK_Depends ):
    return await UserService().auth_vk(uow=uow, params=params)