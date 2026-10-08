from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base, CommonMixin
from app.models.base import InvestmentMixin


class Donation(InvestmentMixin, CommonMixin, Base):
    comment: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('user.id', name='fk_donation_user_id_user'),
        nullable=False
    )
    user = relationship(
        'User',
        back_populates='donations',
    )
