from fastapi import APIRouter, status, Response, Depends, HTTPException, Form
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from user_app.user_services import UserService

# === Schemas
from user_app.schemas import User
from social_acc_app.schemas import OAuth2GoogleUrl, GoogleUserInfo

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
        "url": f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={settings.google_auth.google_client_id}&redirect_uri={settings.google_auth.google_redirect_url}&scope=openid%20profile%20email&access_type=offline"
    }


@router.get(
    "/auth/google",
    status_code=status.HTTP_200_OK,
    response_model=User,
    summary="Создаем Пользователя через учетку Google.",
    description="""
        Данный endpoint сохранен в настройках google console и
        на него настроен редирект после того как пользователь 
        аутентифицируется на стороне Google. После чего будут полученны 
        данные профиля пользователя и сохранены в систему.
    """,
)
async def auth_google(uow: UOF_Depends, code: CodeFromGoogle_Depends):
    data_user_google = await UserService().get_user_info_from_google(code)
    user = await UserService().create_user(
        uow=uow, new_user=data_user_google
    )  # TODO get_or_create?!
    return user
