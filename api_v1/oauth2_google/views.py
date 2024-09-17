from fastapi import APIRouter, status  # Response, Depends, HTTPException, Form
from fastapi.security import OAuth2PasswordBearer  # OAuth2PasswordRequestForm

# === Services
from user_app.user_services import UserService
from email_app.email_services import EmailService
from social_acc_app.social_services import SocialService
from jwt_app.jwt_services import JWTService

# === Schemas
# from user_app.schemas import SaveUserSchema
from social_acc_app.schemas import OAuth2GoogleUrl
from jwt_app.schemas import JWTokensResponse

from core.settings import settings
from api_v1.api_dependencies import UOF_Depends, CodeFromGoogle_Depends


router = APIRouter(tags=["google"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token/")


@router.get(
    "/login/google/",
    status_code=status.HTTP_200_OK,
    response_model=OAuth2GoogleUrl,
    summary="Получить ссылку для авторизации через Google.",
    description="""
        Через данный endpoint можно получить ссылку, 
        которая ведет на страницу авторизации Google.
    """,
)
async def login_google():
    return {
        # TODO вынести в настройки
        "url": f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={settings.google_auth.google_client_id}&redirect_uri={settings.google_auth.google_redirect_url}&scope=openid%20profile%20email&access_type=offline"
    }


@router.get(
    "/auth/google",
    status_code=status.HTTP_200_OK,
    response_model=JWTokensResponse,
    summary="Создаем Пользователя через учетку Google.",
    description="""
        Данный endpoint сохранен в настройках google console и
        на него настроен редирект после того как пользователь 
        аутентифицируется на стороне Google. После чего будут полученны 
        данные профиля пользователя, сохранены в систему, созданы JWT.
    """,
)
async def auth_google(uow: UOF_Depends, code: CodeFromGoogle_Depends):
    return await UserService().auth_google(uow=uow, data_google_form=code)
