import pytest
import pytest_asyncio
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from auth_service.adapters.repositories.repos import OtpModel, UserModel
from auth_service.config import load


@pytest.fixture
def configs():
    configs = load()
    return configs


@pytest_asyncio.fixture()
async def session(configs):
    db_engine = "postgresql+asyncpg"
    engine = create_async_engine(
        f"{db_engine}://{configs.db_config.db_url}", future=True, echo=True
    )
    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    async with async_session() as session:
        yield session


@pytest_asyncio.fixture(autouse=True)
async def clean_db(session):
    yield
    # clean user, otp
    for model in [OtpModel, UserModel]:
        del_stm = delete(model)
        await session.execute(del_stm)
