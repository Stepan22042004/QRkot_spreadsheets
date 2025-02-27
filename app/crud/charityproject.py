from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.charity_project import CharityProject
from app.crud.base import CRUDBase


class CRUDProject(CRUDBase):
    async def get_closed_by_closed_speed(
            self,
            session: AsyncSession,
    ) -> list[dict[str, int]]:

        duration_expr = func.julianday(self.model.close_date) - func.julianday(
            self.model.create_date).label('duration')
        query = (
            select(self.model)
            .add_columns(duration_expr)
            .where(self.model.fully_invested == 1)
            .order_by(duration_expr)
        )
        db_objs = await session.execute(query)
        return db_objs.scalars().all()


charity_project_crud = CRUDProject(CharityProject)
