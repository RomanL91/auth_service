from fastapi import APIRouter

from .oauth2_google.views import router as oath2_google_router


router = APIRouter()

router.include_router(router=oath2_google_router, prefix="/auth_user")
