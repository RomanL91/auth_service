from datetime import datetime

from core import settings


# функция получения времени
def get_current_time():
    return datetime.now(settings.time_zone).replace(tzinfo=None)
