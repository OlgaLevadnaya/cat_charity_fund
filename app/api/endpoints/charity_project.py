import logging

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectUpdate,
    CharityProjectDB
)
from app.models import Donation
from app.api.validators import (
    check_project_name,
    check_project_before_deleting,
    check_project_before_editing
)
from app.crud.charity_project import charity_project_crud
from app.services import check_project_is_close, make_investments


router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_new_charity_project(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session)
):
    await check_project_name(charity_project.name, session)
    new_charity_project = await charity_project_crud.create(
        charity_project, session
    )
    new_charity_project = await make_investments(
        new_charity_project, Donation, session
    )
    logging.info(f'Проект {new_charity_project.name} создан')
    return new_charity_project


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session)
):
    all_charity_projects = await charity_project_crud.get_multi(session)
    return all_charity_projects


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def delete_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    charity_project = await check_project_before_deleting(project_id, session)
    charity_project = await charity_project_crud.remove(
        charity_project, session
    )
    logging.info(f'Проект {charity_project.name} удален')
    return charity_project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def update_charity_project(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),

):
    charity_project = await check_project_before_editing(
        project_id, obj_in, session
    )
    charity_project = await charity_project_crud.update(
        db_obj=charity_project,
        obj_in=obj_in,
        session=session
    )
    charity_project = await check_project_is_close(charity_project, session)
    logging.info(f'Проект {charity_project.name} изменен')
    return charity_project
