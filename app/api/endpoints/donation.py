from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.donation import donation_crud
from app.schemas.donation import (
    DonationCreate, DonationDBCreate, DonationDBGet
)
from app.core.user import current_user
from app.models import User
from app.services.invest import invest_new_donation


router = APIRouter(
    prefix='/donation',
    tags=['Donation'],
)


@router.post(
    '/',
    response_model=DonationDBCreate,
    response_model_exclude_none=True,
)
async def create_new_donation(
        donation: DonationCreate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user),
):
    new_donation = await donation_crud.create(donation, session, user)
    await invest_new_donation(new_donation, session)

    return new_donation


@router.get(
    '/',
    response_model=list[DonationDBGet],
    response_model_exclude_none=True,
)
async def get_all_donations(
        session: AsyncSession = Depends(get_async_session),
):
    return await donation_crud.get_multi(session)


@router.get(
    '/my',
    response_model=list[DonationDBCreate],
    response_model_exclude_none=True,
)
async def get_user_donations(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    return await donation_crud.get_multi(session, user)
