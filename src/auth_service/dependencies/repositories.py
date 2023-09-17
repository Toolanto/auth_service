from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from auth_service.adapters.repositories.repos import PostgresOtpStore, PostgresUserStore
from auth_service.dependencies import configs
from auth_service.repositories import OtpStore, UserStore

db_engine = ""
engine = create_async_engine(
    f"postgresql+asyncpg://{configs.db_config.db_url}", future=True, echo=True
)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


# Dependency
async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session


def get_user_store(session: Annotated[AsyncSession, Depends(get_session)]) -> UserStore:
    return PostgresUserStore(session=session)


def get_otp_store(session: Annotated[AsyncSession, Depends(get_session)]) -> OtpStore:
    return PostgresOtpStore(session=session)
