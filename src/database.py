import asyncio

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from src.settings.config import get_db_url, db_settings

async_engine = create_async_engine(
    url=get_db_url(),
    pool_size=db_settings.DB_POOL_SIZE,
    max_overflow=db_settings.DB_MAX_OVERFLOW,
    echo=False,
)

async_session = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


# async def check_db_health():
#     async with async_session() as session:
#         result = await session.execute(text("SELECT 1"))
#         print(result.scalars().all())
#
# asyncio.run(check_db_health())