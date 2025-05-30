from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charityproject import charity_project_crud
from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.user import current_superuser
from app.schemas.charityproject import CharityProjectDB
from app.services.google_api import (spreadsheets_create,
                                     set_user_permissions,
                                     spreadsheets_update_value)


router = APIRouter(
    prefix='/google',
    tags=['Google']
)


@router.post(
    '/',
    response_model=list[CharityProjectDB],
    dependencies=[Depends(current_superuser)],
)
async def get_report(
        session: AsyncSession = Depends(get_async_session),
        wrapper_services: Aiogoogle = Depends(get_service)

):
    projects = await charity_project_crud.get_closed_by_closed_speed(session)
    spreadsheetid = await spreadsheets_create(wrapper_services)
    await set_user_permissions(spreadsheetid, wrapper_services)
    await spreadsheets_update_value(spreadsheetid,
                                    projects,
                                    wrapper_services)
    return projects
