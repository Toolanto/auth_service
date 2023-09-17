import abc
from datetime import datetime
from typing import Optional

from auth_service.entities.otp import Otp
from auth_service.entities.user import User


class UserStoreErrors:
    class NotFoundError(Exception):
        pass

    class AlreadyExists(Exception):
        pass


class UserStore(abc.ABC):
    @abc.abstractmethod
    async def save(self, user: User) -> User:
        pass  # pragma: no cover

    @abc.abstractmethod
    async def get_by_email(self, email: str) -> User:
        pass  # pragma: no cover

    @abc.abstractmethod
    async def get_by_id(self, id: str) -> User:
        pass  # pragma: no cover


class OtpStoreErrors:
    class NotFoundError(Exception):
        pass

    class AlreadyExists(Exception):
        pass


class OtpStore(abc.ABC):
    @abc.abstractmethod
    async def save(self, otp: Otp) -> Otp:
        pass  # pragma: no cover

    @abc.abstractmethod
    async def get(self, id: str) -> Otp:
        pass  # pragma: no cover

    @abc.abstractmethod
    async def mark_checked(self, otp: Otp) -> None:
        pass  # pragma: no cover

    @abc.abstractmethod
    async def get_valid_otp(self, user_id: str, current_time: datetime) -> Optional[Otp]:
        pass  # pragma: no cover
