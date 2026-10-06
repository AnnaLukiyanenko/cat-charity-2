from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject


class CRUDCharityProject(CRUDBase):

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


charity_project_crud = CRUDCharityProject(CharityProject)
