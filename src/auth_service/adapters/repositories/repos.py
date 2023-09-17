from datetime import datetime
from typing import Optional

import sqlalchemy
from pydantic.dataclasses import dataclass
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import Session, sessionmaker

from auth_service.adapters.repositories.models import OtpModel, UserModel
from auth_service.entities.otp import Otp
from auth_service.entities.store import (
    OtpStore,
    OtpStoreErrors,
    UserStore,
    UserStoreErrors,
)
from auth_service.entities.user import User


@dataclass
class DbConfig:
    db_url: str

    def __post_init__(self):
        db_engine = "postgresql+asyncpg"
        engine = create_async_engine(f"{db_engine}://{self.db_url}", future=True, echo=True)
        self.session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


@dataclass
class PostgresUserStore(UserStore):
    config: DbConfig

    def __post_init__(self):
        self._session: Session = self.config.session

    async def save(self, user: User) -> User:
        try:
            async with self._session() as sess:
                async with sess.begin():
                    sess.add(UserModel(**user.model_dump()))
                    await sess.flush()
                    return user
        except sqlalchemy.exc.IntegrityError:
            raise UserStoreErrors.AlreadyExists("User already exist")

    async def get_by_email(self, email: str) -> User:
        async with self._session() as sess:
            async with sess.begin():
                res = await sess.scalars(select(UserModel).where(UserModel.email == email))
                user = res.first()
                if not user:
                    raise UserStoreErrors.NotFoundError("User not found")
                return User.model_validate(user)

    async def get_by_id(self, id: str) -> User:
        async with self._session() as sess:
            async with sess.begin():
                res = await sess.scalars(select(UserModel).where(UserModel.id == id))
                user = res.first()
                if not user:
                    raise UserStoreErrors.NotFoundError("User not found")
                return User.model_validate(user)


@dataclass
class PostgresOtpStore(OtpStore):
    config: DbConfig

    def __post_init__(self):
        self._session: Session = self.config.session

    async def save(self, otp: Otp) -> Otp:
        try:
            async with self._session() as sess:
                async with sess.begin():
                    sess.add(OtpModel(**otp.model_dump()))
                    await sess.flush()
                    return otp
        except sqlalchemy.exc.IntegrityError:
            raise OtpStoreErrors.AlreadyExists("Otp already exist")

    async def get(self, id: str) -> Otp:
        async with self._session() as sess:
            async with sess.begin():
                res = await sess.scalars(select(OtpModel).where(OtpModel.id == id))
                otp = res.first()
                if not otp:
                    raise OtpStoreErrors.NotFoundError("Otp not found")
                return Otp.model_validate(otp)

    async def mark_checked(self, otp: Otp) -> None:
        async with self._session() as sess:
            async with sess.begin():
                u = update(OtpModel).where(OtpModel.id == otp.id)
                u = u.values(checked=True)
                await sess.execute(u)

    async def get_valid_otp(self, user_id: str, current_time: datetime) -> Optional[Otp]:
        async with self._session() as sess:
            async with sess.begin():
                res = await sess.scalars(
                    select(OtpModel).where(
                        (OtpModel.user_id == user_id)
                        and (OtpModel.checked is False)
                        and (OtpModel.expired > current_time)
                    )
                )
                otp = res.first()
                if not otp:
                    return None
                return Otp.model_validate(otp)
