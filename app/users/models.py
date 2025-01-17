
from fastapi_users.db import SQLAlchemyBaseUserTableUUID

from ..core.database import Base

class User(SQLAlchemyBaseUserTableUUID, Base):
    short_name: str | None = None
    full_name: str | None = None

    def __str__(self):
        return self.short_name or self.full_name or self.email