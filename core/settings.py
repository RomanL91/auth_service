from pytz import timezone as tz

from pathlib import Path
from zoneinfo import ZoneInfo

from pydantic import BaseModel
from pydantic_settings import BaseSettings

from fastapi.middleware.cors import CORSMiddleware


BASE_DIR = Path(__file__).parent.parent


class SettingsAuth(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "public.pem"
    algorithm: str = "RS256"
    token_type: str = "Bearer"
    token_type_field: str = "type"
    access_token_type: str = "access_token"
    refresh_token_type: str = "refresh_token"
    access_token_expire: int = 5  # 5 min
    refresh_token_expire: int = 60 * 24 * 30  # 30 days
    timezone: tz = tz("Asia/Almaty")


class SettingGoogleAuth(BaseModel):
    # TODO .env
    google_client_id: str = (
        "512775846808-npmspbusn7tep886ej4je4n88jrvmqrl.apps.googleusercontent.com"
    )
    google_client_secret: str = "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"
    google_redirect_url: str = "http://localhost:8001/auth_api/v1/auth_user/auth/google"
    # google_redirect_url: str = "https://https://google_oauth2_test.serveo.net/auth_api/v1/auth_user/auth/google"
    google_token_url: str = "https://accounts.google.com/o/oauth2/token"
    google_user_info_url: str = "https://www.googleapis.com/oauth2/v1/userinfo"
    _data_post: dict = {
        "code": None,
        "client_id": google_client_id,
        "client_secret": google_client_secret,
        "redirect_uri": google_redirect_url,
        "grant_type": "authorization_code",
    }
    headers: dict = {"Authorization": None}

    # Геттер для data_post
    @property
    def data_post(self):
        return self._data_post

    # Сеттер для data_post
    @data_post.setter
    def data_post(self, values: dict):
        self._data_post.update(values)

    def get_headers(self, access_token):
        self.headers.update({"Authorization": f"Bearer {access_token}"})
        return self.headers


class SettingVKAuth(BaseModel):
    # TODO .env
    vk_client_id: int = 52285386
    vk_base_url: str = (
        "https://id.vk.com/authorize?response_type=code&client_id=52285386&redirect_uri={vk_redirect_url}&state={state}&code_challenge={code_challenge}&code_challenge_method=s256&scope=email"
    )
    vk_redirect_url: str = (
        "https://google_oauth2_test.serveo.net/auth_api/v1/auth_user/auth/vk"
    )
    vk_token_url: str = "https://id.vk.com/oauth2/auth"
    vk_user_info_url: str = "https://id.vk.com/oauth2/user_info"
    headers: dict = {"Content-Type": "application/x-www-form-urlencoded"}
    # инфа для post запроса на vk_token_url для получения токенов от ВК
    _data_post_request_to_receive_keys: dict = {
        "grant_type": "authorization_code",
        "code_verifier": None,
        "redirect_uri": vk_redirect_url,
        "code": None,
        "client_id": vk_client_id,
        "device_id": None,
        "state": None,
    }
    _information_post_request_to_obtain_user_data: dict = {
        "access_token": None,
        "client_id": vk_client_id,
    }

    # Геттер для data_post_request_to_receive_keys
    @property
    def data_post_request_to_receive_keys(self):
        return self._data_post_request_to_receive_keys

    # Сеттер для data_post_request_to_receive_keys
    @data_post_request_to_receive_keys.setter
    def data_post_request_to_receive_keys(self, values: dict):
        self._data_post_request_to_receive_keys["code_verifier"] = values["state"]
        self._data_post_request_to_receive_keys.update(values)

    def get_data_payload(self, access_token):
        self._information_post_request_to_obtain_user_data.update(
            {"access_token": access_token}
        )
        return self._information_post_request_to_obtain_user_data


class SettingsDataBase(BaseModel):
    url: str = f"sqlite+aiosqlite:///{BASE_DIR}/db.sqlite3"
    echo: bool = True  # Для дебага


class SettingsCORSMiddleware(BaseModel):
    origins: list[str] = ["http://localhost", "http://localhost:3000"]
    middleware: dict = {
        "middleware_class": CORSMiddleware,
        "allow_origins": origins,
        "allow_credentials": True,
        "allow_methods": ["*"],
        "allow_headers": ["*"],
    }


class Settings(BaseSettings):

    # == Other
    api_v1_prefix: str = "/auth_api/v1"
    time_zone: ZoneInfo = ZoneInfo("Asia/Almaty")
    # == DataBase
    db: SettingsDataBase = SettingsDataBase()
    # == Auth
    auth_jwt: SettingsAuth = SettingsAuth()
    # == Google Auth
    google_auth: SettingGoogleAuth = SettingGoogleAuth()
    # == VK Auth
    vk_auth: SettingVKAuth = SettingVKAuth()
    # == CORSMiddleware
    middleware: SettingsCORSMiddleware = SettingsCORSMiddleware()


settings = Settings()
