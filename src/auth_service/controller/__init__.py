from dataclasses import dataclass

from auth_service.entities.user import User
from auth_service.gateway import EmailGateway
from auth_service.repositories import OtpStore, UserStore
from auth_service.usecases.create_user import CreateUserData, CreateUserUsecase
from auth_service.usecases.login_user import (
    LoginUserData,
    LoginUserRes,
    LoginUserUsecase,
)
from auth_service.usecases.otp_login import OtpLoginData, OtpLoginUsecase


@dataclass
class Controller:
    user_store: UserStore
    otp_store: OtpStore
    email_gateway: EmailGateway

    async def create_user(self, req: CreateUserData) -> User:
        return await CreateUserUsecase(user_store=self.user_store).execute(req=req)

    async def login_user(self, req: LoginUserData) -> LoginUserRes:
        return await LoginUserUsecase(
            user_store=self.user_store, otp_store=self.otp_store, email_gateway=self.email_gateway
        ).execute(req=req)

    async def otp_login(self, req: OtpLoginData) -> str:
        return await OtpLoginUsecase(
            user_store=self.user_store,
            otp_store=self.otp_store,
        ).execute(req=req)
