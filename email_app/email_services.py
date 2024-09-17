# == Core
from core.BASE_unit_of_work import IUnitOfWork

# == Exceptions
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

# == Schemas
from email_app.schemas import EmailSchema
from social_acc_app.schemas import DataUserForMyService


class EmailService:
    exclude = (
        "id",
        "first_name",
        "last_name",
        "provider",
        "provider_user_id",
        "ava",
        "active",
    )
    async def create_email(
        self, uow: IUnitOfWork, data_user: DataUserForMyService, **kwargs,
    ) -> EmailSchema | None:
        email_dict = {
            **data_user.model_dump(exclude=self.exclude),
            **kwargs
        }
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
