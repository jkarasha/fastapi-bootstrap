from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession 
from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase

from ..core.database import Base, get_async_session

class User(SQLAlchemyBaseUserTableUUID, Base):
    pass

async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)
