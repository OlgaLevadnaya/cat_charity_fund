from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject
from app.schemas.charity_project import CharityProjectUpdate


async def check_project_name(
    project_name: str,
    session: AsyncSession,
):
    db_project = await session.execute(
        select(CharityProject).where(
            CharityProject.name == project_name
        )
    )
    db_project = db_project.scalars().one_or_none()
    if db_project is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует!',
        )


async def check_project_exists(
        project_id: int,
        session: AsyncSession
):
    db_project = await charity_project_crud.get(
        project_id, session
    )
    if db_project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Проект не найден!',
        )
    return db_project


async def check_project_before_deleting(
        project_id: int,
        session: AsyncSession
):
    db_project = await check_project_exists(
        project_id,
        session
    )
    if db_project.invested_amount > 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='В проект были внесены средства, не подлежит удалению!'
        )
    return db_project


async def check_project_before_editing(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession
):
    db_project = await check_project_exists(
        project_id,
        session
    )
    if db_project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Закрытый проект нельзя редактировать!'
        )
    update_data = obj_in.dict(exclude_unset=True)
    if 'name' in update_data:
        await check_project_name(
            update_data['name'],
            session
        )
    for item in update_data:
        if item not in ['name', 'description', 'full_amount']:
            raise HTTPException(
                status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                detail='Недопустимые поля для обновления!'
            )
    if (
        'full_amount' in update_data and
        update_data['full_amount'] < db_project.invested_amount
    ):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Нельзя установить требуемую сумму меньше уже вложенной!'
        )
    return db_project
