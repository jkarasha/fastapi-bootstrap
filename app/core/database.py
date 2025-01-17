# Refactor code from /db folder into database.py file
from typing import Any

from sqlalchemy import (
    CursorResult,
    Insert,
    MetaData,
    Select,
    Update
)
from sqlalchemy.ext.asyncio import AsyncConnection, create_async_engine
from .config import settings
from .constants import DB_NAMING_CONVENTION

from ..db.base import Base

DATABASE_URL = str(settings.DATABASE_ASYNC_URL)

engine = create_async_engine(
    DATABASE_URL,
    pool_size = settings.DATABASE_POOL_SIZE,
    pool_recycle = settings.DATABASE_POOL_TTL,
    pool_pre_ping = settings.DATABASE_POOL_PRE_PING
)

metadata = MetaData(naming_convention=DB_NAMING_CONVENTION)

async def fetch_one(
    select_query: Select | Insert | Update,
    connection: AsyncConnection | None = None,
    commit_after: bool = False
) -> dict[str, Any] | None:
    if not connection:
        async with engine.connect() as connection:
            cursor = await _execute_query(select_query, connection, commit_after)
            return [r._asdict() for r in cursor.all()]

    cursor = await _execute_query(select_query, connection, commit_after)
    return [r._asdict() for r in cursor.all()]

async def execute(
    query: Insert | Update,
    connection: AsyncConnection = None,
    commit_after: bool = False,
) -> None:
    if not connection:
        async with engine.connect() as connection:
            await _execute_query(query, connection, commit_after)
            return

    await _execute_query(query, connection, commit_after)


async def _execute_query(
    query: Select | Insert | Update,
    connection: AsyncConnection,
    commit_after: bool = False,
) -> CursorResult:
    result = await connection.execute(query)
    if commit_after:
        await connection.commit()

    return result


async def get_db_connection() -> AsyncConnection:
    connection = await engine.connect()
    try:
        yield connection
    finally:
        await connection.close()