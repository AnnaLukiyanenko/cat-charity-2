from fastapi import APIRouter, Depends, HTTPException, status

from app.api.validators import (check_charity_project_exists,
                                check_name_duplicate)
from app.core.db import SessionDep
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectDB,
                                         CharityProjectUpdate)
from app.services.investment import invest

router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def create_charity_project(
    charity_project: CharityProjectCreate,
    session: SessionDep,
):
    """Только для суперюзеров."""
    await check_name_duplicate(
        charity_project.name,
        session,
    )
    new_charity_project = await charity_project_crud.create(
        charity_project,
        session,
    )

    donations = await donation_crud.get_open_objects(session)

    changed_objects = invest(
        new_charity_project,
        donations,
    )
    session.add_all(changed_objects)
    await session.commit()
    await session.refresh(new_charity_project)
    return new_charity_project


@router.get(
    '/',
    response_model=list[CharityProjectDB],
)
async def get_all_charity_projects(
    session: SessionDep,
):
    charity_projects = await charity_project_crud.get_multi(session)
    return charity_projects


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def delete_charity_project(
    project_id: int,
    session: SessionDep,
):
    """Только для суперюзеров."""
    charity_project = await check_charity_project_exists(
        project_id,
        session,
    )

    if charity_project.invested_amount > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='В проект уже были внесены средства!',
        )

    if charity_project.fully_invested:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Нельзя удалить закрытый проект!',
        )

    await charity_project_crud.remove(
        charity_project,
        session,
    )
    await session.commit()

    return charity_project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def update_charity_project(
    project_id: int,
    charity_project: CharityProjectUpdate,
    session: SessionDep,
):
    """Только для суперюзеров."""
    project = await check_charity_project_exists(
        project_id,
        session,
    )

    if project.fully_invested:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Закрытый проект нельзя изменять!',
        )

    if (
        charity_project.full_amount is not None and
        charity_project.full_amount < project.invested_amount
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Нельзя установить сумму меньше уже вложенной!',
        )

    if charity_project.name is not None:
        await check_name_duplicate(
            charity_project.name,
            session,
            project.id,
        )

    updated_project = await charity_project_crud.update(
        project,
        charity_project,
        session,
    )

    donations = await donation_crud.get_open_objects(session)

    changed_objects = invest(
        updated_project,
        donations,
    )
    session.add_all(changed_objects)
    await session.commit()
    await session.refresh(updated_project)

    return updated_project
