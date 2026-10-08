from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy.orm import relationship

from app.core.db import Base, CommonMixin


class User(SQLAlchemyBaseUserTable[int], CommonMixin, Base):
    donations = relationship(
        'Donation',
        back_populates='user',
    )
