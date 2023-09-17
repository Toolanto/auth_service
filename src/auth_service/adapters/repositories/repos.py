from datetime import datetime
from typing import Optional

import sqlalchemy
from pydantic import BaseModel
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from auth_service.adapters.repositories.models import OtpModel, UserModel
from auth_service.entities.otp import Otp
from auth_service.entities.user import User
from auth_service.repositories import (
    OtpStore,
    OtpStoreErrors,
    UserStore,
    UserStoreErrors,
)


class PostgresUserStore(BaseModel, UserStore):
    session: AsyncSession

    class Config:
        arbitrary_types_allowed = True

    async def save(self, user: User) -> User:
        try:
            self.session.add(UserModel(**user.model_dump()))
            await self.session.flush()
            return user
        except sqlalchemy.exc.IntegrityError:
            raise UserStoreErrors.AlreadyExists("User already exist")

    async def get_by_email(self, email: str) -> User:
        res = await self.session.scalars(select(UserModel).where(UserModel.email == email))
        user = res.first()
        if not user:
            raise UserStoreErrors.NotFoundError("User not found")
        return User.model_validate(user)

    async def get_by_id(self, id: str) -> User:
        res = await self.session.scalars(select(UserModel).where(UserModel.id == id))
        user = res.first()
        if not user:
            raise UserStoreErrors.NotFoundError("User not found")
        return User.model_validate(user)


class PostgresOtpStore(BaseModel, OtpStore):
    session: AsyncSession

    class Config:
        arbitrary_types_allowed = True

    async def save(self, otp: Otp) -> Otp:
        try:
            self.session.add(OtpModel(**otp.model_dump()))
            await self.session.flush()
            return otp
        except sqlalchemy.exc.IntegrityError:
            raise OtpStoreErrors.AlreadyExists("Otp already exist")

    async def get(self, id: str) -> Otp:
        res = await self.session.scalars(select(OtpModel).where(OtpModel.id == id))
        otp = res.first()
        if not otp:
            raise OtpStoreErrors.NotFoundError("Otp not found")
        return Otp.model_validate(otp)

    async def mark_checked(self, otp: Otp) -> None:
        u = update(OtpModel).where(OtpModel.id == otp.id)
        u = u.values(checked=True)
        await self.session.execute(u)

    async def get_valid_otp(self, user_id: str, current_time: datetime) -> Optional[Otp]:
        res = await self.session.scalars(
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
