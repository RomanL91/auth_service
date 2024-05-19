from abc import ABC, abstractmethod
from sqlalchemy.engine import Result


from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession


class AbstractRepository(ABC):
    @abstractmethod
    async def create_obj():
        raise NotImplementedError

    @abstractmethod
    async def get_all_objs():
        raise NotImplementedError

    @abstractmethod
    async def get_obj():
        raise NotImplementedError

    @abstractmethod
    async def update_obj():
        raise NotImplementedError

    @abstractmethod
    async def delete_obj():
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_obj(self, data: dict):
        stmt = insert(self.model).values(**data).returning(self.model)
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def get_all_objs(self):
        stmt = select(self.model).order_by(self.model.id)
        result: Result = await self.session.execute(stmt)
        res = result.scalars().all()
        return res

    async def get_obj(self, **filter_by):
        stmt = select(self.model).filter_by(**filter_by)
        res = await self.session.execute(stmt)
        res = res.scalar_one()
        return res

    async def update_obj(self, obj_id: int, data: dict):
        stmt = (
            update(self.model).values(**data).filter_by(id=obj_id).returning(self.model)
        )
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def delete_obj(self, obj_id: int) -> None:
        stmt = delete(self.model).filter_by(id=obj_id)
        await self.session.execute(stmt)
