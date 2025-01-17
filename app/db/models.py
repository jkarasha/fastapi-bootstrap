import os
from dotenv import load_dotenv
from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from sqlalchemy import Column, Integer, String
#
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..db.base import Base

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class User(SQLAlchemyBaseUserTableUUID, Base):
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=True)
    