import abc
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
        pass # pragma: no cover

    @abc.abstractmethod
    async def get(self, email: str) -> User:
        pass # pragma: no cover


class OtpStoreErrors:

    class NotFoundError(Exception):
        pass

    class AlreadyExists(Exception):
        pass


class OtpStore(abc.ABC):
    @abc.abstractmethod
    async def save(self, otp: Otp) -> Otp:
        pass # pragma: no cover

    @abc.abstractmethod
    async def get(self, session_id: str) -> Otp:
        pass # pragma: no cover

    @abc.abstractmethod
    async def mark_checked(self, session_id: str):
        pass # pragma: no cover
