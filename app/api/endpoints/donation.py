from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_user, current_superuser
from app.schemas.donation import (
    DonationCreate,
    DonationDBFull,
    DonationDBShort
)
from app.models import CharityProject, User
from app.crud.donation import donation_crud
from app.services.investment import make_investments


router = APIRouter()


@router.post(
    '/',
    response_model=DonationDBShort,
    response_model_exclude_none=True,

)
async def create_new_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    new_donation = await donation_crud.create(donation, session, user)
    new_donation = await make_investments(
        new_donation, CharityProject, session
    )
    return new_donation


@router.get(
    '/',
    response_model=list[DonationDBFull],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session)
):
    all_donations = await donation_crud.get_multi(session)
    return all_donations


@router.get(
    '/my',
    response_model=list[DonationDBShort],
    response_model_exclude_none=True,
)
async def get_user_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    donations = await donation_crud.get_by_user(session, user)
    return donations
