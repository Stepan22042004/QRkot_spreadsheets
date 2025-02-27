from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Donation, CharityProject
from app.crud.donation import donation_crud
from app.crud.charityproject import charity_project_crud


async def invest_new_donation(
        donation: Donation,
        session: AsyncSession
):

    charity_projects = await charity_project_crud.get_not_fully_invested(
        session)
    now = datetime.now()
    for project in charity_projects:
        available_investment = project.full_amount - project.invested_amount
        investment = min(
            available_investment,
            donation.full_amount - donation.invested_amount
        )

        donation = await donation_crud.invest(
            donation,
            project,
            investment,
            now,
            session
        )
        if donation.invested_amount >= donation.full_amount:
            break


async def invest_to_new_project(
        project: CharityProject,
        session: AsyncSession
):
    donations = await donation_crud.get_not_fully_invested(session)
    now = datetime.now()
    for donation in donations:
        available_investment = project.full_amount - project.invested_amount
        investment = min(
            available_investment,
            donation.full_amount - donation.invested_amount
        )

        project = await charity_project_crud.invest(
            project,
            donation,
            investment,
            now,
            session
        )
        if project.invested_amount == project.full_amount:
            break
