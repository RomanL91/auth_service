import string

from datetime import datetime
from random import choices
from hashlib import sha256
from base64 import urlsafe_b64encode

from core import settings


# ===========================================================
# функция получения времени
def get_current_time():
    return datetime.now(settings.time_zone).replace(tzinfo=None)


# ===========================================================
# ===========================================================
# для OAuth2 VK
# Генерация code_verifier
def generate_code_verifier(length: int = 43) -> str:
    if length < 43 or length > 128:
        raise ValueError("Длина должна быть от 43 до 128 символов")
    characters = string.ascii_letters + string.digits + "_-"
    return "".join(choices(characters, k=length))


# Генерация code_challenge методом S256
def generate_code_challenge(code_verifier: str) -> str:
    # Хешируем verifier методом SHA-256
    sha256_code = sha256(code_verifier.encode("utf-8")).digest()
    # Преобразуем в Base64 без символов '=', '+' и '/'
    return urlsafe_b64encode(sha256_code).rstrip(b"=").decode("utf-8")


# ===========================================================
