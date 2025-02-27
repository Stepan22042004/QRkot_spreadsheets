from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.charityproject import charity_project_crud
from app.schemas.charityproject import (
    CharityProjectCreate, CharityProjectDB, CharityProjectUpdate
)
from app.services.invest import invest_to_new_project
from app.core.user import current_superuser
from app.api.validators import (check_project_same_name,
                                check_project_new_full_amount,
                                check_project_delete_already_invested,
                                check_project_fully_invested,
                                check_project_exists)


router = APIRouter(
    prefix='/charity_project',
    tags=['Charity Projects'],
)


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def create_new_charity_project(
        charity_project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session),
):
    await check_project_same_name(charity_project.name, session)
    new_project = await charity_project_crud.create(charity_project, session)
    await invest_to_new_project(new_project, session)

    return new_project


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
        session: AsyncSession = Depends(get_async_session),
):
    return await charity_project_crud.get_multi(session)


@router.patch(
    '/{charity_project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def partially_update_charity_projects(
        charity_project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    charity_project = await charity_project_crud.get(
        charity_project_id,
        session
    )
    await check_project_exists(charity_project)
    await check_project_fully_invested(charity_project)
    await check_project_new_full_amount(charity_project, obj_in.full_amount)
    await check_project_same_name(obj_in.name, session)
    return await charity_project_crud.update(
        charity_project, obj_in, session
    )


@router.delete(
    '/{charity_project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def remove_charity_project(
        charity_project_id: int,
        session: AsyncSession = Depends(get_async_session),
):

    charity_project = await charity_project_crud.get(
        charity_project_id,
        session
    )
    await check_project_exists(charity_project)
    await check_project_fully_invested(charity_project)
    await check_project_delete_already_invested(charity_project)

    return await charity_project_crud.remove(
        charity_project, session
    )
