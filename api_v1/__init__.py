from fastapi import APIRouter

from .auth_user_api.views import router as auth_user_router


router = APIRouter()

router.include_router(router=auth_user_router, prefix="/auth_user")
