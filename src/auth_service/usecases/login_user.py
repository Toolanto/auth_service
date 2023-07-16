from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel, Field, constr

from auth_service.entities.gateway import EmailGateway
from auth_service.entities.store import OtpStore, UserStore
from auth_service.usecases import get_jwt_token, get_otp


class LoginUserErrors:
    class InvalidCredentials(Exception):
        pass


class LoginUserData(BaseModel):
    email: constr(min_length=1) = Field(..., description="The user email")
    password: constr(min_length=1) = Field(..., description="The user password")


class LoginUserRes(BaseModel):
    otp_id: Optional[str] = None
    token: Optional[str] = None


class LoginUserUsecase(BaseModel):
    user_store: UserStore
    otp_store: OtpStore
    email_gateway: EmailGateway

    class Config:
        arbitrary_types_allowed = True

    async def execute(self, req: LoginUserData) -> LoginUserRes:
        now = datetime.now(tz=timezone.utc)

        user = await self.user_store.get_by_email(email=req.email)
        if not user.is_valid_password(req.password):
            raise LoginUserErrors.InvalidCredentials("Invalid credentials")

        if not user.two_factor_auth_enabled:
            return LoginUserRes(token=get_jwt_token(user=user, current_time=now))

        otp = await self.otp_store.get_valid_otp(user.id, current_time=now)
        if not otp:
            otp = get_otp(user=user, current_time=now)
            await self.otp_store.save(otp=otp)

        body = f"Hi {user.name}, the OTP is {otp.value}"
        await self.email_gateway.send(to_recipient=user.email, subject="OTP", body=body)
        return LoginUserRes(otp_id=otp.id)
