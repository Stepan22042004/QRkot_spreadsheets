from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User


class CRUDBase:

    def __init__(self, model):
        self.model = model

    async def get(
            self,
            obj_id: int,
            session: AsyncSession,
    ):
        db_obj = await session.execute(
            select(self.model).where(
                self.model.id == obj_id
            )
        )
        return db_obj.scalars().first()

    async def get_by_name(
            self,
            name: str,
            session: AsyncSession,
    ):
        db_obj = await session.execute(
            select(self.model).where(
                self.model.name == name
            )
        )
        return db_obj.scalars().first()

    async def get_not_fully_invested(
            self,
            session: AsyncSession,
    ):
        query = select(self.model)
        query = query.order_by(self.model.create_date).where(
            self.model.fully_invested == 0
        )
        db_objs = await session.execute(query)
        return db_objs.scalars().all()

    async def get_multi(
        self,
        session: AsyncSession,
        user: Optional[User] = None
    ):
        query = select(self.model)
        if user is not None:
            query = query.where(self.model.user_id == user.id)
        db_objs = await session.execute(query)
        return db_objs.scalars().all()

    async def create(
            self,
            obj_in,
            session: AsyncSession,
            user: Optional[User] = None
    ):
        obj_in_data = obj_in.dict()
        if user is not None:
            obj_in_data['user_id'] = user.id
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def update(
            self,
            db_obj,
            obj_in,
            session: AsyncSession,
    ):
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(
            self,
            db_obj,
            session: AsyncSession,
    ):
        await session.delete(db_obj)
        await session.commit()
        return db_obj

    async def invest(
            self,
            obj,
            obj_2,
            investment,
            now,
            session: AsyncSession,
    ):
        obj.invested_amount += investment
        obj_2.invested_amount += investment
        if obj_2.invested_amount >= obj_2.full_amount:
            obj_2.fully_invested = True
            obj_2.close_date = now
        if obj.invested_amount >= obj.full_amount:
            obj.fully_invested = True
            obj.close_date = now
        await session.commit()
        await session.refresh(obj)
        return obj
