# == Core
from core.BASE_unit_of_work import IUnitOfWork

# == Exceptions
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError, NoResultFound

# == Schemas
from email_app.schemas import EmailSchema
from social_acc_app.schemas import GoogleUserInfo
from user_app.schemas import SaveUserSchema


class EmailService:
    async def create_email(
        self, uow: IUnitOfWork, google_user: GoogleUserInfo, user: SaveUserSchema
    ) -> EmailSchema | None:
        email_dict = EmailSchema.convert_data(google_user, user).model_dump()
        async with uow:
            try:
                email = await uow.email.create_obj(email_dict)
                await uow.commit()
                return email
            except IntegrityError as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=e,  # TODO пока что показываем ошибки
                )
