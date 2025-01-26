from fastapi import Depends
from sqlalchemy import Column, String
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase

from app.core.database import Base, get_async_session

class User(SQLAlchemyBaseUserTableUUID, Base):
    first_name: str = Column(String(length=128), nullable=True)
    last_name: str = Column(String(length=128), nullable=True)

async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)
