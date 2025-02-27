from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charityproject import charity_project_crud
from app.crud.charityproject import charity_project_crud
from app.models import CharityProject


async def check_project_same_name(name: str,
                                  session: AsyncSession):
    result = await charity_project_crud.get_by_name(name, session)
    if result:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=f"Объекты с именем '{name}' уже существуют"
        )


async def check_project_new_full_amount(project: CharityProject,
                                        new_full_amount: int):
    if new_full_amount and project:
        if new_full_amount < project.invested_amount:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Целевая сумма меньше набранной."
            )


async def check_project_delete_already_invested(project: CharityProject):
    if project:
        if project.invested_amount > 0:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Нельзя удалять проекты с набранной суммой денег."
            )


async def check_project_exists(project: CharityProject):
    if project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Проект не найден!'
        )


async def check_project_fully_invested(project: CharityProject):
    if project.fully_invested is True:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Недопустимая операция'
        )
