__all__ = (
    "DataBaseManager",
    "db_manager",
    "settings",
    "Base",
)

from .DB_manager import DataBaseManager, db_manager
from .settings import settings
from .BASE_model import Base

# for migrations
from auth_user_app.models import User # ставим в комментарий и убираем из миграций
from user_app.models import UserT
from phone_num_app.models import PhoneNumber
from email_app.models import Email
