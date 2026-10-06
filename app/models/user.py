from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable

from app.core.db import Base, CommonMixin


class User(SQLAlchemyBaseUserTable[int], CommonMixin, Base):
    pass
