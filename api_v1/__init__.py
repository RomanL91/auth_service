from fastapi import APIRouter

from .oauth2_google.views import router as oath2_google_router
from .oauth_vk.views import router as oauth2_vk_router


router = APIRouter()

router.include_router(router=oath2_google_router, prefix="/auth_user")
router.include_router(router=oauth2_vk_router, prefix="/auth_user")
