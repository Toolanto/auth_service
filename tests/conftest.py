import pytest
import pytest_asyncio
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from auth_service.adapters.repositories.repos import DbConfig, OtpModel, UserModel
from auth_service.config import load


@pytest.fixture
def configs():
    configs = load()
    return configs


@pytest.fixture
def db_config(configs):
    return DbConfig(**configs.db_config.model_dump())


@pytest_asyncio.fixture(autouse=True)
async def clean_db(configs):
    db_engine = "postgresql+asyncpg"
    engine = create_async_engine(
        f"{db_engine}://{configs.db_config.db_url}", future=True, echo=True
    )
    session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    yield
    # clean user, otp
    async with session() as sess:
        async with sess.begin():
            for model in [OtpModel, UserModel]:
                del_stm = delete(model)
                await sess.execute(del_stm)
