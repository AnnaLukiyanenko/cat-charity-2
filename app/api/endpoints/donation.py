from typing import Annotated

from fastapi import APIRouter, Depends

from app.core.db import SessionDep
from app.core.user import current_superuser, current_user
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.models.user import User
from app.schemas.donation import (DonationCreate, DonationCreateResponse,
                                  DonationFullInfoDB, DonationUserDB)
from app.services.investment import invest

router = APIRouter()


@router.post(
    '/',
    response_model=DonationCreateResponse,
)
async def create_donation(
    donation: DonationCreate,
    session: SessionDep,
    user: Annotated[User, Depends(current_user)],
):
    new_donation = await donation_crud.create(
        donation,
        session,
        user
    )

    projects = await charity_project_crud.get_open_objects(session)

    changed_objects = invest(
        new_donation,
        projects,
    )

    session.add_all(changed_objects)
    await session.commit()
    await session.refresh(new_donation)

    return new_donation


@router.get(
    '/',
    response_model=list[DonationFullInfoDB],
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
    session: SessionDep,
):
    """Только для суперюзеров."""
    donations = await donation_crud.get_multi(session)
    return donations


@router.get(
    '/my',
    response_model=list[DonationUserDB],
)
async def get_my_donations(
    session: SessionDep,
    user: Annotated[User, Depends(current_user)],
):
    donations = await donation_crud.get_by_user(
        session,
        user,
    )
    return donations
