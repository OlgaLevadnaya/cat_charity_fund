from datetime import datetime

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session


async def make_investments(
    new_object,
    model,
    session: AsyncSession = Depends(get_async_session),
):
    full_amount_new_object = new_object.full_amount
    existed_objects = await session.execute(
        select(model).where(
            model.fully_invested == 0
        )
    )
    for existed_object in existed_objects.scalars().all():
        if full_amount_new_object == 0:
            break
        needed_amount_existed_object = (
            existed_object.full_amount - existed_object.invested_amount
        )
        if needed_amount_existed_object <= full_amount_new_object:
            existed_object.invested_amount += needed_amount_existed_object
            full_amount_new_object -= needed_amount_existed_object
            existed_object.fully_invested = True
            existed_object.close_date = datetime.now()
            session.add(existed_object)
        else:
            existed_object.invested_amount += full_amount_new_object
            full_amount_new_object = 0

    new_object.fully_invested = full_amount_new_object == 0
    new_object.close_date = (
        datetime.now() if new_object.fully_invested else None
    )
    new_object.invested_amount = (
        new_object.full_amount - full_amount_new_object
    )
    session.add(new_object)
    await session.commit()
    await session.refresh(new_object)
    return new_object
