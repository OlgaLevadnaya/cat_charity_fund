from datetime import datetime

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.models import CharityProject


async def check_project_is_close(
        project: CharityProject,
        session: AsyncSession = Depends(get_async_session),):
    if project.full_amount == project.invested_amount:
        project.close_date = datetime.now()
        project.fully_invested = True
    session.add(project)
    await session.commit()
    await session.refresh(project)
    return project
