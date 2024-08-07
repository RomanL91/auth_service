from pytz import timezone as tz

from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings


BASE_DIR = Path(__file__).parent.parent


class SettingsAuth(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "public.pem"
    algorithm: str = "RS256"
    token_type: str = "Bearer"
    token_type_field: str = "type"
    access_token_type: str = "access"
    refresh_token_type: str = "refresh"
    access_token_expire: int = 5  # 5 min
    refresh_token_expire: int = 60 * 24 * 30  # 30 days
    timezone: tz = tz("Asia/Almaty")


class SettingGoogleAuth(BaseModel):
    # TODO .env
    google_client_id: str = (
       ""
    )
    google_client_secret: str = ""
    google_redirect_url: str = ""
    google_token_url: str = ""
    google_user_info_url: str = ""
    data_post: dict = {
        "code": None,
        "client_id": google_client_id,
        "client_secret": google_client_secret,
        "redirect_uri": google_redirect_url,
        "grant_type": "authorization_code",
    }
    headers: dict = {"Authorization": None}

    def get_data_to_post(self, code):
        self.data_post.update({"code": code})
        return self.data_post

    def get_headers(self, access_token):
        self.headers.update({"Authorization": f"Bearer {access_token}"})
        return self.headers


class SettingsDataBase(BaseModel):
    url: str = f"sqlite+aiosqlite:///{BASE_DIR}/db.sqlite3"
    echo: bool = True  # Для дебага


class Settings(BaseSettings):
    api_v1_prefix: str = "/auth_api/v1"

    # == DataBase
    db: SettingsDataBase = SettingsDataBase()
    # == Auth
    auth_jwt: SettingsAuth = SettingsAuth()
    # == Google Auth
    google_auth: SettingGoogleAuth = SettingGoogleAuth()


settings = Settings()
