from uuid import uuid4

from httpx import AsyncClient

from pydantic import BaseModel

from user_app.schemas import User
from social_acc_app.schemas import GoogleUserInfo, VKUserInfo, DataUserForMyService


# Адаптер для Google
class GoogleAdapter:
    @staticmethod
    def to_user(google_data: GoogleUserInfo) -> DataUserForMyService:
        return DataUserForMyService(
            id=uuid4(),
            first_name=google_data.given_name,
            last_name=google_data.family_name,
            email=google_data.email,
            provider="google",
            provider_user_id=google_data.id,
            ava=google_data.picture,
        )

# Адаптер для VK
class VKAdapter:
    @staticmethod
    def to_user(vk_data: VKUserInfo) -> DataUserForMyService:
        return DataUserForMyService(
            id=uuid4(),
            first_name=vk_data.first_name,
            last_name=vk_data.last_name,
            email=vk_data.email,
            provider="vk",
            provider_user_id=vk_data.user_id,
            ava=vk_data.avatar,
        )
    

# Фабрика адаптеров
class UserFactoryAdapter:
    @staticmethod
    def create_user(data: BaseModel, source: str) -> User:
        if source == "google":
            return GoogleAdapter.to_user(data)
        elif source == "vk":
            return VKAdapter.to_user(data)
        else:
            raise ValueError(f"Unsupported source: {source}")
        
    @staticmethod
    async def fetch_user_info(
        url: str,
        headers: dict = None,
        data: dict = None,
        request_method: str = "GET"
    ):
        client = AsyncClient()
        # Выбираем метод запроса (GET или POST)
        if request_method == "POST":
            response = await client.post(url, headers=headers, data=data)
            user_info_response = response.json().get("user")
            return VKUserInfo(**user_info_response)
        else:
            response = await client.get(url, headers=headers)
            user_info_response = response.json()
            return GoogleUserInfo(**user_info_response)