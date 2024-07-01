from pytz import timezone as tz

from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings


BASE_DIR = Path(__file__).parent.parent


class SettingsAuth(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "public.pem"
    algoritm: str = "RS256"
    token_type: str = "Bearer"
    access_token_type: str = "access"
    refresh_token_type: str = "refresh"
    access_token_expire: int = 5
    refresh_token_expire: int = 60 * 24 * 30 # 30 days
    timezone: tz = tz('Asia/Almaty')


class SettingsDataBase(BaseModel):
    url: str = f"sqlite+aiosqlite:///{BASE_DIR}/db.sqlite3"
    echo: bool = True  # Для дебага


class Settings(BaseSettings):
    api_v1_prefix: str = "/auth_api/v1"

    # == DataBase
    db: SettingsDataBase = SettingsDataBase()
    # == Auth
    auth_jwt: SettingsAuth = SettingsAuth()


settings = Settings()
