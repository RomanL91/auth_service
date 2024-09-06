# == Core
from core.BASE_unit_of_work import IUnitOfWork

# == Exceptions
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError, NoResultFound

# == Schemas
from social_acc_app.schemas import SocialAccountSchema, GoogleUserInfo
from user_app.schemas import SaveUserSchema
from email_app.schemas import SaveEmailSchema


class SocialService:
    async def create_social_acc(self, uow: IUnitOfWork, google_user: GoogleUserInfo, user: SaveUserSchema, email: SaveUserSchema) -> SocialAccountSchema | None:
        social_acc_dict = SocialAccountSchema.convert_data(google_user, user, email).model_dump()
        async with uow:
            try:
                social = await uow.social.create_obj(social_acc_dict)
                await uow.commit()
                return social
            except IntegrityError as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=e,  # TODO пока что показываем ошибки
                )       
