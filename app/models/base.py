from datetime import datetime

from sqlalchemy import Boolean, CheckConstraint, DateTime, Integer
from sqlalchemy.orm import Mapped, declared_attr, mapped_column


class InvestmentMixin:

    def __init__(self, **kwargs):
        kwargs.setdefault('invested_amount', 0)
        kwargs.setdefault('fully_invested', False)
        super().__init__(**kwargs)

    @declared_attr
    def __table_args__(cls):
        return (
            CheckConstraint(
                'full_amount > 0',
                name=f'check_{cls.__tablename__}_full_amount_positive',
            ),
            CheckConstraint(
                'invested_amount >= 0 AND invested_amount <= full_amount',
                name=f'check_{cls.__tablename__}_invested_amount_range',
            ),
        )

    full_amount: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    invested_amount: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    fully_invested: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    create_date: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    close_date: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )
