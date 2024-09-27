from fastapi import APIRouter

from .oauth2_google.views import router as oath2_google_router
from .oauth_vk.views import router as oauth2_vk_router
from .auth_phone.views import router as auth_phone_router
from .user.views import router as user_router
from .jwt.views import router as jwt_router

router = APIRouter()

router.include_router(router=oath2_google_router, prefix="/auth_user")
router.include_router(router=oauth2_vk_router, prefix="/auth_user")
router.include_router(router=auth_phone_router, prefix="/auth_user")
router.include_router(router=user_router, prefix="/user")
router.include_router(router=jwt_router, prefix="/token")
