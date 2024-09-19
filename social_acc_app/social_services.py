# == Core
from core.BASE_unit_of_work import IUnitOfWork

# == Exceptions
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

# == Schemas
from social_acc_app.schemas import SocialAccountSchema, DataUserForMyService


class SocialService:
    exclude = (
        "ava",
        "last_name",
        "first_name",
        "email",
        "active",
    )

    async def create_social_acc(
        self,
        uow: IUnitOfWork,
        data_user: DataUserForMyService,
        **kwargs,
    ) -> SocialAccountSchema | None:
        social_acc_dict = {
            **data_user.model_dump(exclude=self.exclude),
            **kwargs,
        }
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
        
    async def get_social_acc_by_provider_and_user_id(
        self,
        uow: IUnitOfWork,
        provider: str,
        user_id: str,
    ):
        async with uow:
            social_accont = await uow.social.get_social_acc_by_provider_and_user_id(
                provider=provider,
                user_id=user_id,
            )
            return social_accont
