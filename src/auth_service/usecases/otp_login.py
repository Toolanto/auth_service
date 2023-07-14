from datetime import datetime, timezone

from pydantic import BaseModel, Field, constr

from auth_service.entities.store import OtpStore, OtpStoreErrors, UserStore
from auth_service.usecases import get_jwt_token


class OtpLoginErrors:
    class InvalidCredentials(Exception):
        pass


class OtpLoginData(BaseModel):
    otp_id: constr(min_length=1) = Field(
        ..., description="The OTP id. Only for user with 2FA enabled."
    )
    otp: constr(min_length=1) = Field(..., description="The OTP value received by email.")


class OtpLoginUsecase(BaseModel):
    user_store: UserStore
    otp_store: OtpStore

    class Config:
        arbitrary_types_allowed = True

    async def execute(self, req: OtpLoginData) -> str:
        try:
            otp = await self.otp_store.get(id=req.otp_id)
        except OtpStoreErrors.NotFoundError:
            raise OtpLoginErrors.InvalidCredentials("Invalid OTP")

        current_time = datetime.now(tz=timezone.utc)
        if not otp.is_valid_otp(otp=req.otp, current_time=current_time):
            raise OtpLoginErrors.InvalidCredentials("Invalid OTP")

        user = await self.user_store.get(email=otp.user_email)
        jwt_token = get_jwt_token(user=user, current_time=current_time)

        await self.otp_store.mark_checked(otp=otp)
        return jwt_token
